from .decomposer import decompose_task

if __name__ == "__main__":
    msg = "Summarize this announcement and then plan my evening study."
    result = decompose_task(msg)
    print(result)