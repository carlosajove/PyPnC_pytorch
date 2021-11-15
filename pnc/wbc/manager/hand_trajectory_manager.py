import numpy as np
from util import util
from util import interpolation

class HandTrajectoryManager(object):
    def __init__(self, pos_task, ori_task, robot):
        self._pos_task = pos_task
        self._ori_task = ori_task
        self._robot = robot

        assert self._pos_task.target_id == self._ori_task.target_id
        self._target_id = self._pos_task.target_id

        self._start_moving_time = 0.
        self._moving_duration = 0.

        self._pos_hermite_curve = None
        self._quat_hermite_curve = None

    def update_desired(self, target_hand_iso):
        hand_pos_des = target_hand_iso[0:3, 3]
        hand_vel_des = np.zeros(3)
        hand_acc_des = np.zeros(3)

        hand_ori_des = util.rot_to_quat(target_hand_iso[0:3, 0:3])
        hand_ang_vel_des = np.zeros(3)
        hand_ang_acc_des = np.zeros(3)

        self._pos_task.update_desired(hand_pos_des, hand_vel_des, hand_acc_des)
        self._ori_task.update_desired(hand_ori_des, hand_ang_vel_des,
                                      hand_ang_acc_des)

    def use_current(self):
        current_hand_iso = self._robot.get_link_iso(self._target_id)
        current_hand_vel = self._robot.get_link_vel(self._target_id)

        hand_pos_des = current_hand_iso[0:3, 3]
        hand_vel_des = current_hand_vel[3:6]
        hand_acc_des = np.zeros(3)

        hand_ori_des = util.rot_to_quat(current_hand_iso[0:3, 0:3])
        hand_ang_vel_des = current_hand_vel[0:3]
        hand_ang_acc_des = np.zeros(3)

        self._pos_task.update_desired(hand_pos_des, hand_vel_des, hand_acc_des)
        self._ori_task.update_desired(hand_ori_des, hand_ang_vel_des,
                                      hand_ang_acc_des)

    def initialize_hand_trajectory(self, start_time, duration,
                                   target_hand_iso):
        self._start_moving_time = start_time
        self._moving_duration = duration

        init_hand_iso = self._robot.get_link_iso(self._target_id)
        init_hand_vel = self._robot.get_link_vel(self._target_id)

        init_hand_quat = util.rot_to_quat(init_hand_iso[0:3, 0:3])
        target_hand_quat = util.rot_to_quat(target_hand_iso[0:3, 0:3])

        self._pos_hermite_curve = interpolation.HermiteCurveVec(
            init_hand_iso[0:3, 3], init_hand_vel[3:6], target_hand_iso[0:3, 3],
            np.zeros(3))
        self._quat_hermite_curve = interpolation.HermiteCurveQuat(
            init_hand_quat, init_hand_vel[0:3], target_hand_quat, np.zeros(3))

    def update_hand_trajectory(self, current_time):
        ##interpolation
        s = (current_time - self._start_moving_time) / self._moving_duration
        hand_pos_des = self._pos_hermite_curve.evaluate(s)
        hand_vel_des = self._pos_hermite_curve.evaluate_first_derivative(s)
        hand_acc_des = self._pos_hermite_curve.evaluate_second_derivative(s)

        hand_quat_des = self._quat_hermite_curve.evaluate(s)
        hand_ang_vel_des = self._quat_hermite_curve.evaluate_ang_vel(s)
        hand_ang_acc_des = self._quat_hermite_curve.evaluate_ang_acc(s)

        self._pos_task.update_desired(hand_pos_des, hand_vel_des, hand_acc_des)
        self._ori_task.update_desired(hand_quat_des, hand_ang_vel_des, hand_ang_acc_des)