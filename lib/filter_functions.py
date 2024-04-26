def is_may_be_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False
    
def is_may_be_dict(text: str) -> bool:
    try:
        dictionary = eval(text)
        print(dictionary)
        if isinstance(dictionary, dict):
            return True
        else:
            return False
    except:
        return False
    

def main():
    text = "{'key': 'value'}"

    print(is_may_be_dict(text))



if __name__ == "__main__":
    main()