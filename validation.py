
class Validation:
    def __init__(self):
        pass


    def pnrvalidate(self,element):
        if element:
            element = str(element).strip()
            return len(element) == 6 and element.isalnum()
        else:
            return False


    def mobilevalidate(self,element):
        if element:
            return len(element) == 10 and element.isdigit()
        else:
            return False