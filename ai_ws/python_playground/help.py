def help():
    from pathlib import Path

    url = "./__langchain/knowledges/MH Markets/test.pdf"
    if url.startswith("./"):
        url = url[2:]
    print(url.split("/"))
    [org, domain] = url.split("/")
    print(org, domain)
