class BusError(Exception):
    pass


class CommunicationError(Exception):
    pass


class GenericError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


def check_error(error_code):
    """
    Check the error code of a VME communication and raise the appropriate exception.
    """
    if error_code == 0:
        return
    if error_code == -1:
        raise BusError()
    if error_code == -2:
        raise CommunicationError()
    if error_code == -3:
        raise GenericError()
    if error_code == -4:
        raise InvalidParameterError()
    if error_code == -5:
        raise TimeoutError()
