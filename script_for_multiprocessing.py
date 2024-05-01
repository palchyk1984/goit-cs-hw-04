from multiprocessing import Process, Queue
import os
import time

def search_in_file(file_path, keywords, queue):
    """Search for keywords in a single file and count their occurrences."""
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
        for keyword in keywords:
            count = content.count(keyword)
            if count > 0:
                results[keyword] = [(file_path, count)]
    except Exception as e:
        results['error'] = str(e)
    queue.put(results)

def process_files(file_chunks, keywords, queue):
    for file_path in file_chunks:
        search_in_file(file_path, keywords, queue)

def main_multiprocessing(files, keywords):
    num_processes = 4
    process_list = []
    queue = Queue()
    file_chunks = [files[i::num_processes] for i in range(num_processes)]

    start_time = time.time()
    for i in range(num_processes):
        process = Process(target=process_files, args=(file_chunks[i], keywords, queue))
        process_list.append(process)
        process.start()

    result_dict = {}
    for process in process_list:
        process.join()

    while not queue.empty():
        results = queue.get()
        for key, value in results.items():
            if key in result_dict:
                result_dict[key].extend(value)
            else:
                result_dict[key] = value

    print(f"Elapsed time: {time.time() - start_time}s")
    return result_dict

if __name__ == '__main__':
    directory = os.getcwd()
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    keywords = ["urgent", "confidential", "important"]
    results = main_multiprocessing(files, keywords)
    print(results)
