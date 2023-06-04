class service:
    def __init__(self,id:int,name:str) -> None:
        """Represents

        Args:
            id (int): _description_
            name (str): _description_
        """        
        self.id=id
        self.name=name
        
twitter=service(0,"Twitter")
reddit=service(1,"Reddit")