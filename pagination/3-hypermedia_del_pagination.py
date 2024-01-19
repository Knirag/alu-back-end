def get_hyper_index(self, current_index: int = None, page_size: int = 10) -> Dict:
    """
    Get the hyper index.

    Args:
        current_index: Current index.
        page_size: Total size of the page.

    Return:
        Hyper index.
    """
    result_dataset = []
    index_data = self.indexed_dataset()
    keys_list = list(index_data.keys())
    assert current_index + page_size < len(keys_list)
    assert current_index < len(keys_list)

    if current_index not in index_data:
        start_index = keys_list[current_index]
    else:
        start_index = current_index

    for i in range(start_index, start_index + page_size):
        if i not in index_data:
            result_dataset.append(index_data[keys_list[i]])
        else:
            result_dataset.append(index_data[i])

    next_index: int = current_index + page_size

    if current_index in keys_list:
        next_index
    else:
        next_index = keys_list[next_index]

    return {
        'index': current_index,
        'next_index': next_index,
        'page_size': len(result_dataset),
        'data': result_dataset
    }
