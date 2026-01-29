
class Objects():
    def __init__(self, x = -1, y = -1, id_tag = -1, render_tag = -1, name = "Unknown object"):
        self.id_tag = id_tag
        self.render_tag = render_tag
        self.shaded_render_tag = -render_tag
        self.name = name
        self.description = ""
        self.traits = {"object": True}
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def has_trait(self, trait):
        if trait in self.traits:
            return self.traits[trait]
        else:
            return False

    def gain_ID(self, ID):
        self.id_tag = ID

    def get_location(self):
        return (self.x,self.y)

    def get_distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**2)**(1/2)

    def get_render_tag(self):
        return self.render_tag

    def get_id_tag(self):
        return self.id_tag

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.name

    def get_render_text(self):
        return [self.name, self.description]

    def get_is_in_square(self, x_start, x_end, y_start, y_end):
        if self.get_x() >= x_start and self.get_x() < x_end and self.get_y()>= y_start and self.get_y() < y_end:
            return True
        else:
            return False

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def set_render_tag(self, render_tag):
        self.render_tag = render_tag


