from flask_sqlalchemy import SQLAlchemy




class item():
    def __init__(self, _name, _description, _price, _priority) -> None:
        self.Name = _name
        self.Description = _description
        self.Price = _price
        self.Priority = _priority
    def getItemInfo(self):
        return [self.Name, self.Description, self.Price, self.Priority]
    
class preferences():
    def __init__(self, _color1, _color2, _color3, 
                 _shirtSize, _pantSizeLength, _pantSizeWidth,
                 _womensPantsSize, _shoeSize, _ringSize,
                 _jewleryMetalType) -> None:
        self.color1 = _color1
        self.color2 = _color2
        self.color3 = _color3
        self.shirtSize = _shirtSize
        self.pantSizeLength = _pantSizeLength
        self.pantSizeWidth = _pantSizeWidth
        self.womensPantsSize = _womensPantsSize
        self.shoeSize = _shoeSize
        self.ringSize = _ringSize
        self.jewleryMetalType = _jewleryMetalType