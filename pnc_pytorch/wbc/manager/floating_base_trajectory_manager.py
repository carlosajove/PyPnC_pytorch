import numpy as np
import torch

from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

from util import util
from util import interpolation


class FloatingBaseTrajectoryManager(object):
    def __init__(self, batch, com_task, base_ori_task, robot):
        self._n_batch = batch
        self._com_task = com_task
        self._base_ori_task = base_ori_task
        self._robot = robot

        self._start_time = torch.zeros(self._n_batch)
        self._duration = torch.zeros(self._n_batch)
        self._ini_com_pos, self._target_com_pos = torch.zeros(self._n_batch, 3), torch.zeros(self._n_batch, 3)
        self._ini_base_quat, self._target_base_quat = np.zeros(4), np.zeros(4)

        self._amp = np.zeros(3)
        self._freq = np.zeros(3)

        self._b_swaying = False

    @property
    def b_swaying(self):
        return self._b_swaying

    @b_swaying.setter
    def b_swaying(self, value):
        self._b_swaying = value


    #TODO: make pytorch if needed
    def initialize_floating_base_interpolation_trajectory(
            self, start_time, duration, target_com_pos, target_base_quat):
        self._start_time = start_time
        self._duration = duration

        self._ini_com_pos = self._robot.get_com_pos()
        self._target_com_pos = target_com_pos

        #TODO: change when rot
        target_base_quat = target_base_quat[0].numpy()
        self._ini_base_quat = util.rot_to_quat(
            self._robot.get_link_iso(self._base_ori_task.target_id)[0,0:3, 0:3].numpy())
        self._target_base_quat = target_base_quat
        # self._quat_error= (R.from_quat(self._target_base_quat) *
        # R.from_quat(self._ini_base_quat).inv()).as_quat() # Sign flipped
        self._quat_error = R.from_matrix(
            np.dot(
                R.from_quat(self._target_base_quat).as_matrix(),
                R.from_quat(
                    self._ini_base_quat).as_matrix().transpose())).as_quat()
        self._exp_error = util.quat_to_exp(self._quat_error)

        """
        np.set_printoptions(precision=5)
        print("ini com: ", self._ini_com_pos)
        print("end com: ", self._target_com_pos)
        print("ini quat: ", self._ini_base_quat)
        print("end quat: ", self._target_base_quat)
        """

    def update_floating_base_desired(self, current_time):
        com_pos_des, com_vel_des, com_acc_des = torch.zeros(self._n_batch, 3), torch.zeros(self._n_batch, 3), torch.zeros(self._n_batch, 3)

        for i in range(3):
            com_pos_des[i] = interpolation.smooth_changing_pytorch(
                self._ini_com_pos[i], self._target_com_pos[i],
                self._duration, current_time - self._start_time)
            com_vel_des[i] = interpolation.smooth_changing_vel_pytorch(
                self._ini_com_pos[i], self._target_com_pos[i],
                self._duration, current_time - self._start_time)
            com_acc_des[i] = interpolation.smooth_changing_acc_pytorch(
                self._ini_com_pos[i], self._target_com_pos[i],
                self._duration, current_time - self._start_time)

        self._com_task.update_desired(com_pos_des, 
                                      com_vel_des, 
                                      com_acc_des)

        scaled_t = interpolation.smooth_changing_pytorch(
            torch.zeros(self._n_batch), torch.ones(self._n_batch), self._duration, current_time - self._start_time)
        scaled_tdot = interpolation.smooth_changing_vel_pytorch(
            torch.zeros(self._n_batch), torch.ones(self._n_batch), self._duration, current_time - self._start_time)
        scaled_tddot = interpolation.smooth_changing_acc_pytorch(
            torch.zeros(self._n_batch), torch.ones(self._n_batch), self._duration, current_time - self._start_time)



        scaled_t = scaled_t[0].numpy()
        scaled_tddot = scaled_tddot[0].numpy()
        scaled_tdot = scaled_tdot[0].numpy()
        exp_inc = self._exp_error * scaled_t
        quat_inc = util.exp_to_quat(exp_inc)

        # TODO (Check this again)
        # base_quat_des = R.from_matrix(
        # np.dot(
        # R.from_quat(quat_inc).as_matrix(),
        # R.from_quat(self._ini_base_quat).as_matrix())).as_quat()
        base_quat_des = R.from_matrix(
            np.dot(
                R.from_quat(self._ini_base_quat).as_matrix(),
                R.from_quat(quat_inc).as_matrix())).as_quat()
        base_angvel_des = self._exp_error * scaled_tdot
        base_angacc_des = self._exp_error * scaled_tddot

        self._base_ori_task.update_desired(torch.from_numpy(base_quat_des).expand(self._n_batch, -1), 
                                           torch.from_numpy(base_angvel_des).expand(self._n_batch, -1),
                                           torch.from_numpy(base_angacc_des).expand(self._n_batch, -1))