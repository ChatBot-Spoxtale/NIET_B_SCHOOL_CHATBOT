memory = []


def add(role, content):
    memory.append({"role": role, "content": content})
    if len(memory) > 10:
        memory.pop(0)


def get():
    return memory
