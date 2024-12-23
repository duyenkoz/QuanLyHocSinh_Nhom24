def calcPagination(page_index, total_pages, visible_links=5):
    pagination = []

    if total_pages <= visible_links:
        pagination = list(range(1, total_pages + 1))
    else:
        if page_index <= visible_links // 2:
            pagination = list(range(1, visible_links + 1)) + ["..."] + [total_pages]
        elif page_index > total_pages - visible_links // 2:
            pagination = [1, "..."] + list(range(total_pages - visible_links + 1, total_pages + 1))
        else:
            pagination = [1, "..."] + \
                         list(range(page_index - visible_links // 2, page_index + visible_links // 2 + 1)) + \
                         ["...", total_pages]

    return pagination
