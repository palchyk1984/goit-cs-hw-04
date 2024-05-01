import threading
from pathlib import Path
import time

def search_keywords_in_file(file_path, keywords):
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in results:
                        results[keyword] = []
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return results

def thread_function(files, keywords, result_dict, lock):
    local_results = {}
    for file in files:
        results = search_keywords_in_file(file, keywords)
        for keyword, paths in results.items():
            if keyword in local_results:
                local_results[keyword].extend(paths)
            else:
                local_results[keyword] = paths
    with lock:
        for keyword, paths in local_results.items():
            if keyword in result_dict:
                result_dict[keyword].extend(paths)
            else:
                result_dict[keyword] = paths

def main_threading(path, keywords):
    start_time = time.time()
    files = list(Path(path).rglob('*.txt'))
    num_threads = 4
    files_per_thread = len(files) // num_threads
    threads = []
    results = {}
    lock = threading.Lock()

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = start_index + files_per_thread if i != num_threads - 1 else len(files)
        thread_files = files[start_index:end_index]
        thread = threading.Thread(target=thread_function, args=(thread_files, keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Elapsed time: {time.time() - start_time}s")
    return results

# Використовуйте цю частину коду для запуску функції
if __name__ == '__main__':
    keywords = ["urgent", "confidential", "important"]
    results = main_threading('text_files', keywords)
    print(results)
