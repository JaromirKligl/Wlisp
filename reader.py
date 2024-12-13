def get_reader_table():
    return {
        '(' : 'list-start',
        ')': 'list-end',
        ' ': 'whitespace',
        '\n': 'whitespace',
        '\t' : 'whitespace',
        '\r': 'whitespace',
        '\'' : 'quote',
        '#' : 'dispatch',
        '#\'' : 'function',
        '#c' : 'complex',}


def reader(text):
    current_char = 0
    length = len(text)
    init_list = ['progn']
    reader_table = get_reader_table()
    symbol_buff = []

    def handle_dispatch(list):
        nonlocal current_char
        char = text[current_char]
        current_char += 1
        match reader_table[f"#{char}"]:
            case 'complex':
                current_char += 1
                return read_list([reader_table[f"#{char}"]])
            case _:
                return read_char(reader_table[f"#{char}"])

    def read_char(prev=None, buff=None):

        nonlocal current_char



        if prev:
            buffer = (buff or [prev])
        else:
            buffer = (buff or [])

        if current_char == length:
            if buffer:
                return [buffer[0], "".join(buffer[1:])]
            return buff

        char = text[current_char]
        current_char += 1

        if char in reader_table:
            match reader_table[char]:
                case'list-start':
                    return buffer + [(read_list([]))]

                case'whitespace':
                    return [buffer[0], "".join(buffer[1:])]

                case 'list-end':
                    current_char -= 1
                    return [buffer[0], "".join(buffer[1:])]

        return read_char(buff=buffer + [char])


    def read_list(list):
        nonlocal current_char
        nonlocal symbol_buff

        while current_char < length:
            char = text[current_char]
            current_char += 1
            if char in reader_table:
                match reader_table[char]:
                    case 'list-start':
                        list.append(read_list([]))
                    case 'list-end':
                        if symbol_buff:
                            list.append("".join(symbol_buff))
                            symbol_buff = []

                        return list

                    case 'whitespace':
                        if symbol_buff:
                            list.append("".join(symbol_buff))
                            symbol_buff = []

                    case 'dispatch':
                        list.append(handle_dispatch(list))
                    case _:
                        list.append(read_char(prev=reader_table[char]))
            else:
                symbol_buff.append(char)

        if symbol_buff:
            list.append("".join(symbol_buff))
        return list

    return read_list(['progn'])