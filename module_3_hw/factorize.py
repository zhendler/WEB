import time
import multiprocessing

def factorize_sequential(numbers):
    results = []
    for num in numbers:
        factors = set()
        for i in range(1, int(num**0.5) + 1):
            if num % i == 0:
                factors.add(i)
                factors.add(num // i)
        results.append(sorted(factors))
    return results

def factorize_parallel(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(factorize_sequential, [numbers])
    return results[0]

def test():
    a, b, c, d = factorize_parallel([128, 255, 99999, 10651060])
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

if __name__ == '__main__':
    numbers = [128, 255, 99999, 10651060] * 1000

    # Sequential execution
    start_time = time.time()
    sequential_result = factorize_sequential(numbers)
    end_time = time.time()
    print("Sequential time:", end_time - start_time)

    # Parallel execution
    start_time = time.time()
    parallel_result = factorize_parallel(numbers)
    end_time = time.time()
    print("Parallel time:", end_time - start_time)

    test()