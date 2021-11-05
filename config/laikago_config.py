import numpy as np


class SimConfig(object):
    CONTROLLER_DT = 0.01
    N_SUBSTEP = 10
    KP = 0.
    KD = 0.

    INITIAL_POS_WORLD_TO_BASEJOINT = [0, 0, 0.5]
    INITIAL_QUAT_WORLD_TO_BASEJOINT = [0.5, 0.5, 0.5, 0.5]

    PRINT_ROBOT_INFO = True


class PnCConfig(object):
    CONTROLLER_DT = SimConfig.CONTROLLER_DT
    SAVE_DATA = True
    SAVE_FREQ = 1

    PRINT_ROBOT_INFO = SimConfig.PRINT_ROBOT_INFO


class WBCConfig(object):
    # Max normal force per contact
    RF_Z_MAX = 400.0

    # Task Hierarchy Weights
    W_COM = 10.0
    W_BASE_ORI = 20.0
    W_CONTACT_FOOT = 60.0
    W_SWING_FOOT = 40.0

    # Task Gains
    KP_COM = np.array([100., 100., 100])
    KD_COM = np.array([10., 10., 10.])

    KP_BASE_ORI = np.array([100., 100., 100])
    KD_BASE_ORI = np.array([10., 10., 10.])

    KP_FOOT_POS = np.array([400., 400., 400.])
    KD_FOOT_POS = np.array([40., 40., 40.])

    # Regularization terms
    LAMBDA_Q_DDOT = 1e-8
    LAMBDA_RF = 1e-7

    B_TRQ_LIMIT = True

    # Integration Parameters
    VEL_CUTOFF_FREQ = 2.0  #Hz
    POS_CUTOFF_FREQ = 1.0  #Hz
    MAX_POS_ERR = 0.2  #Radians


class PushRecoveryConfig(object):
    INIT_STAND_DUR = 1.0
    RF_Z_MAX_TIME = 0.2
    INITIAL_COM_POS = np.array([0., 0., 0.4])
    INITIAL_BASE_ORI = np.array([0.5, 0.5, 0.5, 0.5])


class PushRecoveryState(object):
    STAND = 0
    BALANCE = 1
