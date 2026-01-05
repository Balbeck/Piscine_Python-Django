class Intern:
    def __init__(self, name=None) -> None:
        self.Name = name or "My name? I’m nobody, an intern, I have no name."     # Attribut
    
    def __str__(self) -> str:
        return self.Name
    
    class Coffee:
        def __str__(self) -> str:
            return "This is the worst coffee you ever tasted."

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")
    
    def make_coffee(self) -> Coffee:
        return self.Coffee()



def test():

    try :
        intern = Intern()
        print(intern)
        mark = Intern("Mark")
        print(mark)
        intern.work()
    except Exception as e:
        print(e)

    try :
        coffee = mark.make_coffee()
        print(coffee)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    test()
