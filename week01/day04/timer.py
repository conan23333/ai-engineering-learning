import time
from collections.abc import Callable
from typing import TypeVar
from exceptions import RetryableError,RetryExhaustedError,NonRetryableError
T=TypeVar("T")

def creat_timer(reponsecode):
    code="200"
    def timer()->bool:
        start = time.time()
        time.sleep(1)
        end = time.time()
        print(f"函数耗时{end-start}")
        if(reponsecode=="400"):
            raise RetryableError()
        if(reponsecode=="500"):
             raise NonRetryableError();
        return code
    return timer
def retry(creat_timer: Callable[[],T],max_attempts:int) -> T:
        for attempt in range(max_attempts+1):
            try:
                return creat_timer()
            except RetryableError:
                print(f"第{attempt}次失败，重试")
        raise RetryExhaustedError()

if __name__=="__main__":
    retry1 = creat_timer("500")
    retry(retry1,5)