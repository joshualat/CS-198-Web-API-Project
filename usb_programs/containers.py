import wx

class Container(object):
    def __init__(self, parent, img, parent_bitmap, action, x=0, y=0):
        self.parent = parent
        self.set_images(img)
        my_region = wx.RegionFromBitmap(self.img)
        self.region = wx.RegionFromBitmap(parent_bitmap)
        self.region.IntersectRegion(my_region)
        self.action = action
        self.x = 0
        self.y = 0
        self.move_to(x, y)
        self.press_level = 'none'
        self.set_press_level('off')
    
    def set_images(self, img):
    
        self.img_name = img
        self.images = {
            'off':       wx.Bitmap(img + '.png',   wx.BITMAP_TYPE_PNG),
            'highlight': wx.Bitmap(img + '_s.png', wx.BITMAP_TYPE_PNG),
            'press':     wx.Bitmap(img + '_p.png', wx.BITMAP_TYPE_PNG),
        }
        self.img = self.images['off']
        
    def hide(self):
        w, h = self.size()
        self.set_pos(-w - 1, -h - 1)
        return self
        
    def set_pos(self, x, y):
        self.reset_pos()
        self.move_to(x, y)
        return self
    
    def reset_pos(self):
        self.move_to(-self.x, -self.y)
        return self
        
    def move_to(self, x, y):
        self.x += x
        self.y += y
        self.region.Offset(x, y)
        return self
        
    def set_press_level(self, press_level):
        if self.press_level != press_level:
            self.press_level = press_level
            self.p_img = self.images[press_level] 
            return True
        return False
    
    def GetWidth(self):
        return self.img.GetWidth()
    
    def GetHeight(self):
        return self.img.GetHeight()
        
    def size(self):
        return (self.GetWidth(), self.GetHeight())
    
    def OnPaint(self, dc):
        dc.DrawBitmap(self.p_img, self.x, self.y, True)
        
    def __str__(self):
        return self.img_name
   

class GlassyContainer(Container):
    def __init__(self, parent, glass, icon, img, parent_bitmap, action, x=0, y=0):
        self.parent = parent
        self.glass = glass
        self.icon = icon
        super(GlassyContainer, self).__init__(parent, img, parent_bitmap, action, x, y)
        
    def move_to(self, x, y):
        super(GlassyContainer, self).move_to(x, y)
        gw = self.glass.GetWidth()
        gh = self.glass.GetHeight()
        w, h = self.size()
        self.gx = self.x + (w - gw) / 2
        self.gy = self.y + (h - gh) / 2
    
    def OnPaint(self, dc):
        super(GlassyContainer, self).OnPaint(dc)
        if self.press_level != 'off':
            dc.DrawBitmap(self.glass, self.gx, self.gy, True)
            self.parent.draw_icon(dc, self.icon)

class Label(Container):
    def __init__(self, parent, img, parent_bitmap, x=0, y=0):
        super(Label, self).__init__(parent, img, parent_bitmap, (lambda: 0), x, y)
        self.p_img = self.img
        
    def set_press_level(self, press_level):
        self.press_level = press_level
        return False
    
    def set_images(self, img):
        self.img_name = img
        self.img = wx.Bitmap(img + '.png', wx.BITMAP_TYPE_PNG)