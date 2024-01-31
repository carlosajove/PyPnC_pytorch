import abc

import torch

class Task(abc.ABC):
    """
    WBC Task
    --------
    Usage:
        update_desired --> update_jacobian --> update_cmd
    """
    def __init__(self, robot, dim, n_batch):
        self._robot = robot
        self._dim = dim
        self.n_batch = n_batch

        self._w_hierarchy = 1.0

        self._kp = torch.zeros(self._dim)  #kp and kd will be the same fro all robots
        self._kd = torch.zeros(self._dim)  #since they don't change during sim, can change this eventually

        self._jacobian = torch.zeros(self.n_batch, self._dim, self._robot.n_q_dot)
        self._jacobian_dot_q_dot = torch.zeros(self.n_batch, self._dim)

        self._op_cmd = torch.zeros(self.n_batch, self._dim)
        self._pos_err = torch.zeros(self.n_batch, self._dim)

        self._pos_des = torch.zeros(self.n_batch, self._dim)
        self._vel_des = torch.zeros(self.n_batch, self._dim)
        self._acc_des = torch.zeros(self.n_batch, self._dim)

    @property
    def op_cmd(self):
        return self._op_cmd

    @property
    def pos_err(self):
        return self._pos_err

    @property
    def pos_des(self):
        return self._pos_des

    @pos_des.setter
    def pos_des(self, val):
        self._pos_des = val

    @property
    def jacobian(self):
        return self._jacobian

    @property
    def jacobian_dot_q_dot(self):
        return self._jacobian_dot_q_dot

    @property
    def kp(self):
        return self._kp

    @property
    def kd(self):
        return self._kd

    @property
    def w_hierarchy(self):
        return self._w_hierarchy

    @property
    def dim(self):
        return self._dim

    @kp.setter
    def kp(self, value):
        assert value.shape[0] == self._dim
        self._kp = value

    @kd.setter
    def kd(self, value):
        assert value.shape[0] == self._dim
        self._kd = value

    @w_hierarchy.setter
    def w_hierarchy(self, value):
        self._w_hierarchy = value

    def update_desired(self, pos_des, vel_des, acc_des):
        """
        Update pos_des, vel_des, acc_des which will be used later to compute
        op_cmd

        Parameters
        ----------
        pos_des (torch.tensor([nbatch, size])):
            For orientation task, the size of torch tensor (2nd variable) is 4, and it should
            be represented in scalar-last quaternion
        vel_des (torch.tensor([nbatch, size])):
            Velocity desired
        acc_des (torch.tensor([nbatch, size])):
            Acceleration desired
        """
        assert vel_des.shape[1] == self._dim
        assert acc_des.shape[1] == self._dim
        self._pos_des = pos_des
        self._vel_des = vel_des
        self._acc_des = acc_des

    @abc.abstractmethod
    def update_cmd(self):
        """
        Update op_cmd given updated pos_des, vel_des, acc_des
        """
        pass

    @abc.abstractmethod
    def update_jacobian(self):
        """
        Update jacobian and jacobian_dot_q_dot
        """
        pass

    def debug(self):
        print("pos des: ", self._pos_des)
        print("pos err: ", self._pos_err)
        print("vel des: ", self._vel_des)
        print("acc des: ", self._acc_des)
        print("xddot: ", self._op_cmd)
