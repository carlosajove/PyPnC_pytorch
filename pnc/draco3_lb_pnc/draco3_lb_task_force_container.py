import numpy as np

from config.draco3_lb_config import WBCConfig, PnCConfig
from pnc.task_force_container import TaskForceContainer
from pnc.wbc.basic_task import BasicTask
from pnc.wbc.basic_contact import SurfaceContact


class Draco3LBTaskForceContainer(TaskForceContainer):
    def __init__(self, robot):
        super(Draco3LBTaskForceContainer, self).__init__(robot)

        # ======================================================================
        # Initialize Task
        # ======================================================================
        # COM Task
        self._com_task = BasicTask(robot, "COM", 3, 'com', PnCConfig.SAVE_DATA)
        self._com_task.kp = WBCConfig.KP_COM
        self._com_task.kd = WBCConfig.KD_COM
        self._com_task.w_hierarchy = WBCConfig.W_COM

        # Torso position task
        # self._torso_pos_task = BasicTask(robot, "LINK_XYZ", 3,
        # 'torso_com_link', PnCConfig.SAVE_DATA)
        # self._torso_pos_task.kp = WBCConfig.KP_COM
        # self._torso_pos_task.kd = WBCConfig.KD_COM
        # self._torso_pos_task.w_hierarchy = WBCConfig.W_COM

        # Torso orientation task
        self._torso_ori_task = BasicTask(robot, "LINK_ORI", 3,
                                         "torso_com_link", PnCConfig.SAVE_DATA)
        self._torso_ori_task.kp = WBCConfig.KP_TORSO
        self._torso_ori_task.kd = WBCConfig.KD_TORSO
        self._torso_ori_task.w_hierarchy = WBCConfig.W_TORSO

        # Rfoot Pos Task
        self._rfoot_pos_task = BasicTask(robot, "LINK_XYZ", 3,
                                         "r_foot_contact", PnCConfig.SAVE_DATA)
        self._rfoot_pos_task.kp = WBCConfig.KP_FOOT_POS
        self._rfoot_pos_task.kd = WBCConfig.KD_FOOT_POS
        self._rfoot_pos_task.w_hierarchy = WBCConfig.W_CONTACT_FOOT

        # Lfoot Pos Task
        self._lfoot_pos_task = BasicTask(robot, "LINK_XYZ", 3,
                                         "l_foot_contact", PnCConfig.SAVE_DATA)
        self._lfoot_pos_task.kp = WBCConfig.KP_FOOT_POS
        self._lfoot_pos_task.kd = WBCConfig.KD_FOOT_POS
        self._lfoot_pos_task.w_hierarchy = WBCConfig.W_CONTACT_FOOT

        # Rfoot Ori Task
        self._rfoot_ori_task = BasicTask(robot, "LINK_ORI", 3,
                                         "r_foot_contact", PnCConfig.SAVE_DATA)
        self._rfoot_ori_task.kp = WBCConfig.KP_FOOT_ORI
        self._rfoot_ori_task.kd = WBCConfig.KD_FOOT_ORI
        self._rfoot_ori_task.w_hierarchy = WBCConfig.W_CONTACT_FOOT

        # Lfoot Ori Task
        self._lfoot_ori_task = BasicTask(robot, "LINK_ORI", 3,
                                         "l_foot_contact", PnCConfig.SAVE_DATA)
        self._lfoot_ori_task.kp = WBCConfig.KP_FOOT_ORI
        self._lfoot_ori_task.kd = WBCConfig.KD_FOOT_ORI
        self._lfoot_ori_task.w_hierarchy = WBCConfig.W_CONTACT_FOOT

        self._task_list = [
            self._com_task, self._torso_ori_task, self._rfoot_pos_task,
            self._lfoot_pos_task, self._rfoot_ori_task, self._lfoot_ori_task
        ]

        # ======================================================================
        # Initialize Contact
        # ======================================================================
        # Rfoot Contact
        self._rfoot_contact = SurfaceContact(robot, "r_foot_contact", 0.1,
                                             0.04, 0.3, PnCConfig.SAVE_DATA)
        self._rfoot_contact.rf_z_max = 1e-3  # Initial rf_z_max
        # Lfoot Contact
        self._lfoot_contact = SurfaceContact(robot, "l_foot_contact", 0.1,
                                             0.04, 0.3, PnCConfig.SAVE_DATA)
        self._lfoot_contact.rf_z_max = 1e-3  # Initial rf_z_max

        self._contact_list = [self._rfoot_contact, self._lfoot_contact]

    @property
    def com_task(self):
        return self._com_task

    # @property
    # def torso_pos_task(self):
    # return self._torso_pos_task

    @property
    def torso_ori_task(self):
        return self._torso_ori_task

    @property
    def rfoot_pos_task(self):
        return self._rfoot_pos_task

    @property
    def lfoot_pos_task(self):
        return self._lfoot_pos_task

    @property
    def rfoot_ori_task(self):
        return self._rfoot_ori_task

    @property
    def lfoot_ori_task(self):
        return self._lfoot_ori_task

    @property
    def rfoot_contact(self):
        return self._rfoot_contact

    @property
    def lfoot_contact(self):
        return self._lfoot_contact

    @property
    def task_list(self):
        return self._task_list

    @property
    def contact_list(self):
        return self._contact_list
