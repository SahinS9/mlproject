import sys
from typing import Optional

def build_error_message(
        error: Exception
        ,error_detail: Optional[object] = None
) -> str:
    "error message with file name and line number"
    detail = error_detail or sys

    _, _, traceback = detail.exc_info()

    if traceback is None:
        return str(error)
    
    file_name = traceback.tb_frame.f_code.co_filename
    line_number = traceback.tb_lineno

    return(
        f"Error occured in file [{file_name}],"
        f"line {line_number}: {error}"
    )


class CustomException(Exception):

    def __init__(
            self
            ,error: Exception
            ,error_detail: Optional[object] = None

    ) -> None:
        self.error_message = build_error_message(
            error=error
            ,error_detail=error_detail
        )

        super().__init__(self.error_message) #Initialize the built-in Exception part of my CustomException object

    def __str__(self) -> str:
        return self.error_message