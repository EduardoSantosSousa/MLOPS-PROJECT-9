import  traceback
import sys 

class CustomException(Exception):

    def __init__(self, error_message, erro_detail):
        super().__init__(error_message)
        self.eror_message = self.get_detailed_error_message(error_message, erro_detail)


    @staticmethod
    def get_detailed_error_message(erro_message, erro_detail:sys):
        #Getting the exception type, value and traceback

        _,_, exc_tb = traceback.sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        #capture the full traceback
        tb_str = "".join(traceback.format_exception(*sys.exc_info()))

        #Including the full traceback in the message:
        return f"Erro in {file_name}, line {line_number}: {erro_message} \n\n Original Traceback:\n{tb_str}"


    def __str__(self):
        return self.eror_message    