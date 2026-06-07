import contextlib
import joblib
from tqdm import tqdm
import time


@contextlib.contextmanager
def tqdm_joblib(tqdm_object: tqdm):
    """Context manager to patch joblib to report into tqdm progress bar.

    Args:
        tqdm_object: The tqdm instance to update.
    """

    class TqdmBatchCompletionCallBack(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallBack
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def parallel_run(
    func, arg_list: list, n_jobs: int = -1, desc: str = "Processing", **kwargs
) -> list:
    """Executes a function in parallel with joblib and monitors progress with tqdm.

    Args:
        func: The function to be executed in parallel.
        arg_list: A list of arguments to pass to the function.
            Each element can be a single value, a tuple (positional args),
            or a dictionary (keyword args).
        n_jobs: The number of jobs to run in parallel. Default is -1 (all CPUs).
        desc: The description for the progress bar. Default is "Processing".
        **kwargs: Additional arguments passed to joblib.Parallel.

    Returns:
        A list of results from the function execution.
    """

    def wrapper(args):
        if isinstance(args, dict):
            return func(**args)
        if isinstance(args, (list, tuple)):
            return func(*args)
        return func(args)

    with tqdm_joblib(tqdm(total=len(arg_list), desc=desc)):
        return list(
            joblib.Parallel(n_jobs=n_jobs, **kwargs)(
                joblib.delayed(wrapper)(args) for args in arg_list
            )
        )


if __name__ == "__main__":
    # Sample task: heavy computation simulation
    def sample_task(x: int) -> int:
        time.sleep(0.1)
        return x * x

    # Execute
    data = list(range(50))
    print("Starting parallel task...")
    # batch_size=1 ensures smooth progress bar updates
    results = parallel_run(sample_task, data, n_jobs=-1, batch_size=1)
    print(f"Results (first 5): {results[:5]} ...")
