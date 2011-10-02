#!/usr/bin/python

# gui_main.pyw

import wx
from containers import *
from util import *
from help import *
from info import *

SPACING = 3
GROUP_SPACING = 15
BAR_SIZE = 21
MAIN_YOFF_INP = 110
CROSS_DX = 7
CROSS_DY = 5
BUTTON_DX = 20
BUTTON_DY = 20
BUTTON_SPACING_X = 3
BUTTON_SPACING_Y = 3
PANEL_XOFF = 20
PANEL_YOFF = 40
PANEL_INPUT_DX = 0
PANEL_INPUT_DY = 20
INPUT_DX = 2
INPUT_DY = 2
MSG_OX = 36
MSG_OY = 55
ICON_DX = 40
ICON_DY = 70
TEXT_LEN = 400
TEXT_SIZE = 11
STAT_SPACING = 10
INPUT_X = 300

class Gui(wx.Frame):
    @verify_first
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, style=wx.FRAME_SHAPED | wx.SIMPLE_BORDER)# | wx.FRAME_NO_TASKBAR)
        self.font = wx.Font(TEXT_SIZE, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
            wx.FONTWEIGHT_BOLD, False, 'Comic Sans MS')
        self.bitmap = wx.Bitmap('screen/main.png', wx.BITMAP_TYPE_PNG)
        self.glass = wx.Bitmap('misc/selector.png', wx.BITMAP_TYPE_PNG)
        self.container_state = {}
        self.mouse_pos = None
        self.move_drag = False
        self.delta = None
        self.containers = None
        self.widget_map = {}
        self.message = None
        self.state = None
        self.text_x = 0
        self.text_y = 0
        self.c_message = None
        
        w = self.bitmap.GetWidth()
        h = self.bitmap.GetHeight()
        self.SetClientSize((w, h))

        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetFShape)
        else: self.SetFShape()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        
        exit_c = Container(self, 'misc/cross', self.bitmap, self.Close)
        exit_c.move_to(w - exit_c.GetWidth() - CROSS_DX, CROSS_DY)
        
        
        self.required = Label(self, 'text/label/required', self.bitmap)
        self.fail = Label(self, 'text/label/fail', self.bitmap)
        self.succ = Label(self, 'text/label/succ', self.bitmap)
        self.wait = Label(self, 'text/label/wait', self.bitmap)
        self.warning = Label(self, 'text/label/warning_keys', self.bitmap)
        self.inone = wx.Bitmap('icon/none.png', wx.BITMAP_TYPE_PNG)
        
        
        containers = [exit_c]
        groups = [
            [
                ('edit_info', 'edit', 'editinfo'),
                ('change_pass', 'newpass', 'newpass'),
            ],
            [
                ('reg', 'reg', 'register'),
                ('login_out', 'site', 'login_out'),
            ],
            [
                ('gen', 'gen', 'gen'),
            ],
            [
                ('help', 'help', 'help'),
            ],
        ]
        y = MAIN_YOFF_INP
        for group in groups:
            for path, state, icon in group:
                icon = wx.Bitmap('icon/' + icon + '.png', wx.BITMAP_TYPE_PNG)
                x = ICON_DX + icon.GetWidth() + GROUP_SPACING
                g_cont = self.get_glassy_container(self.bitmap, 'text/menu/' + path, icon, x, y, state)
                containers.append(g_cont)
                y += g_cont.GetHeight() + SPACING
            y += GROUP_SPACING
        
        self.container_state['main'] = (self.bitmap, containers, [], [], lambda: 0, {})
        
        
        
        
        containers = [exit_c]
        bitmap = wx.Bitmap('screen/editinfo.png', wx.BITMAP_TYPE_PNG)
        containers.extend([self.required, self.succ, self.fail])
        widget_map, widgets, more_containers = self.widgets(
            ('first_name', []),
            ('last_name', []),
            ('email', []),
            ('sex', [x[0] for x in GENDER_CHOICES]),
            ('birthdate', []),
            ('address', []),
            ('country', ['', 'Philippines', 'Japan', 'USA']),
            ('contact_number', []),
        );
        containers.extend(more_containers)
        apply = Container(self, 'text/button/apply', self.bitmap, self.edit_info)
        ok = Container(self, 'text/button/ok', self.bitmap, self.edit_info_ok)
        cancel = Container(self, 'text/button/cancel', self.bitmap, self.get_set_state('main'))
        self.container_state['edit'] = (bitmap, containers, [apply, ok, cancel], widgets, self.edit_info_init, widget_map)
        
        
        
        
        containers = [exit_c]
        bitmap = wx.Bitmap('screen/gen.png', wx.BITMAP_TYPE_PNG)
        containers.extend([self.warning, self.wait, self.succ, self.fail])
        yes = Container(self, 'text/button/yes', self.bitmap, self.gen_crypt_data)
        no = Container(self, 'text/button/no', self.bitmap, self.get_set_state('main'))
        self.container_state['gen'] = (bitmap, containers, [yes, no], [], self.gen_init, {})
        
        
        
        
        containers = [exit_c]
        bitmap = wx.Bitmap('screen/help.png', wx.BITMAP_TYPE_PNG)
        containers.append(Label(self, 'text/label/help', self.bitmap, MSG_OX, MSG_OY))
        ok = Container(self, 'text/button/ok', self.bitmap, self.get_set_state('main'))
        self.container_state['help'] = (bitmap, containers, [ok], [], lambda: 0, {})
        
        
        
        
        containers = [exit_c]
        bitmap = wx.Bitmap('screen/login_out.png', wx.BITMAP_TYPE_PNG)
        containers.extend([self.required, self.succ, self.fail])
        widget_map, widgets, more_containers = self.widgets(
            ('choosewebsite', self.get_websites),
        );
        containers.extend(more_containers)
        login = Container(self, 'text/button/login', self.bitmap, self.login)
        logout = Container(self, 'text/button/logout', self.bitmap, self.logout)
        update = Container(self, 'text/button/updateinfo', self.bitmap, self.update_info)
        cancel = Container(self, 'text/button/cancel', self.bitmap, self.get_set_state('main'))
        self.container_state['site'] = (bitmap, containers, [login, logout, update, cancel], widgets, self.init_websites, widget_map)
        
        
        
        
        containers = [exit_c]
        bitmap = wx.Bitmap('screen/reg.png', wx.BITMAP_TYPE_PNG)
        widget_map, widgets, more_containers = self.widgets(
            ('enterwebsite', []),
            ('username', []),
        );
        containers.extend(more_containers)
        register = Container(self, 'text/button/register', self.bitmap, self.register)
        containers.extend([self.required, self.succ, self.fail])
        cancel = Container(self, 'text/button/cancel', self.bitmap, self.get_set_state('main'))
        self.container_state['reg'] = (bitmap, containers, [register, cancel], widgets, lambda: 0, widget_map)
        
        
        containers = [exit_c]
        bitmap = wx.Bitmap('screen/change_pass.png', wx.BITMAP_TYPE_PNG)
        containers.append(Label(self, 'text/label/notimplemented', self.bitmap, MSG_OX, MSG_OY))
        cancel = Container(self, 'text/button/cancel', self.bitmap, self.get_set_state('main'))
        self.container_state['newpass'] = (bitmap, containers, [cancel], [], lambda: 0, {})
        
        
        self.set_state('main')
        
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, True)
        
        self.Centre()
        self.Show(True)
    
    def edit_info_ok(self):
        self.edit_info()
        if self.successful:
            self.set_state('main')
    
    def edit_info(self):
        self.start_op() 
        try:
            usb_data = SecureFileIO.load_usb_data()
            successful = True
            for field, field_tuple in fields.items(): 
                name, choices, required = field_tuple
                widget = self.widget_map[field]
                usb_data[field] = widget.GetValue()
                if required and not usb_data[field]:
                    successful = False
                    x, y = widget.GetPosition()
                    self.required.set_pos(x + widget.GetSize()[0] + INPUT_DX, y)
                    break
            if successful:
                self.successful = successful
                SecureFileIO.save_usb_data(usb_data)
        except Exception, e:
            self.c_message.append(str(e))
        finally:
            self.success_handle()
    
    def edit_info_init(self):
        usb_data = SecureFileIO.load_usb_data()
        for field, field_tuple in fields.items():
            if usb_data.has_key(field):
                widget = self.widget_map[field]
                if hasattr(widget, "ChangeValue"):
                    widget.ChangeValue(usb_data[field])
                else:
                    widget.SetValue(usb_data[field])
    
    def gen_init(self):
        self.warning.set_pos(MSG_OX, MSG_OY)
        
    def login(self):
        ''' logins to website '''
        self.start_op() 
        conn = None
        try:
            widget = self.widget_map['choosewebsite']
            url = widget.GetValue()  
            if not url:
                x, y = widget.GetPosition()
                self.required.set_pos(x + widget.GetSize()[0] + INPUT_DX, y)
            else:
                conn = SecureWebConnection(url, hashed_password())
                conn.start()
                page = conn.secure_message('login')
                self.successful = page['success']
                self.message = page['message']
        except Exception, e:
            self.c_message.append(str(e))
        finally:
            if conn:
                conn.end()
            self.success_handle()
    
    def logout(self):
        ''' logouts from website '''
        self.start_op()
        conn = None
        try:
            widget = self.widget_map['choosewebsite']
            url = widget.GetValue()  
            if not url:
                x, y = widget.GetPosition()
                self.required.set_pos(x + widget.GetSize()[0] + INPUT_DX, y)
            else:
                conn = SecureWebConnection(url, hashed_password())
                conn.start()
                page = conn.secure_message('logout')
                self.successful = page['success']
                self.message = page['message']
        except Exception, e:
            self.c_message.append(str(e))
        finally:
            if conn:
                conn.end()
            self.success_handle()
        
    
    def register(self):
        self.start_op()
        ''' registers to website '''
        conn = None
        try:
            widget = None
            for name in ['enterwebsite', 'username']:
                if widget:
                    break;
                w = self.widget_map[name]
                if not w.GetValue():
                    widget = w
            if widget:
                x, y = widget.GetPosition()
                self.required.set_pos(x + widget.GetSize()[0] + INPUT_DX, y)
            else:
                url = self.widget_map['enterwebsite'].GetValue()
                conn = SecureWebConnection(url, hashed_password())
                conn.start()
                usb_data = usb_data_for_site()
                username = self.widget_map['username'].GetValue()
                usb_data['username'] = username
                page = conn.secure_message('username_exists',username=username)
                if not page['success']:
                    self.message = 'Username already exists.'
                else:
                    page = conn.secure_message('register', **usb_data)
                    if page['success']:
                        SecureFileIO.update_usb_usernames(conn.url, usb_data['username'])
                        self.successful = True
                    else:
                        self.message = page['message']
        except Exception, e:
            self.c_message.append(str(e))
        finally:
            if conn:
                conn.end()
            self.success_handle()
    
    def update_info(self):
        self.start_op()
        conn = None
        try:
            widget = self.widget_map['choosewebsite']
            url = widget.GetValue()  
            if not url:
                x, y = widget.GetPosition()
                self.required.set_pos(x + widget.GetSize()[0] + INPUT_DX, y)
            else:
                conn = SecureWebConnection(url, hashed_password())
                conn.start()    
                user_info = usb_data_for_site(conn.url)
                page = conn.secure_message('edit_user_info', **user_info)
                self.successful = page['success']
                self.message = page['message']
        except Exception, e:
            self.c_message.append(str(e))
        finally:
            if conn:
                conn.end()
            self.success_handle()
    
    def gen_crypt_data(self):
        self.start_op()
        self.containers[2], self.text_x, self.text_y = self.buttons(self.containers[0], [])
        self.text_x = self.bitmap.GetWidth() - TEXT_LEN
        self.Refresh()
        try:
            start_time = ConsoleTools.start_timer()
            priv_key, pub_key = PKA.generate_keys()
            total_time = ConsoleTools.end_timer(start_time)
            ConsoleTools.file_write('box/private.key',priv_key)
            ConsoleTools.file_write('box/public.key',pub_key)
            uuid = SecTools.generate_uuid()
            salt = SecTools.generate_salt()
            text = uuid + "\n" + salt
            ConsoleTools.file_write('box/config',text)
            self.successful = True
        except Exception, e:
            self.c_message.append(str(e))
        finally:
            ok = Container(self, 'text/button/ok', self.bitmap, self.get_set_state('main'))
            self.containers[2], self.text_x, self.text_y = self.buttons(self.containers[0], [ok])
            self.text_x = self.bitmap.GetWidth() - TEXT_LEN
            self.Refresh()
            wx.Sleep(100)
            self.success_handle()
        
    def start_op(self):
        self.required.hide()
        self.succ.hide()
        self.fail.hide()
        self.wait.set_pos(self.warning.x, self.warning.y)
        self.warning.hide()
        self.successful = False
        self.message = None
        self.c_message = []
        self.Refresh()
    
    def success_handle(self):
        label = self.succ if self.successful else self.fail 
        label.set_pos(MSG_OX, self.text_y 
                    - STAT_SPACING - self.fail.GetHeight())
        self.wait.hide()
        self.warning.hide()
        if not self.successful:
            self.c_message.append('message: ' + str(self.message))
        self.Refresh()
        
    def get_websites(self):
        return get_sites()
    
    def widgets(self, *args):
        x = PANEL_XOFF + PANEL_INPUT_DX
        y = PANEL_YOFF + PANEL_INPUT_DY
        widgets = []
        containers = []
        widget_map = {}
        for path, choices in args:
            c_label = Label(self, 'text/info/' + path, self.bitmap, x, y)
            containers.append(c_label)
            w, h = c_label.size()
            if choices:
                c_info = wx.ComboBox(self, -1, pos=(x + w + INPUT_DX, y), 
                    choices = choices() if callable(choices) else choices, 
                    size = (-1, c_label.GetHeight()),
                    style=wx.CB_READONLY)
            else:
                c_info = wx.TextCtrl(self, pos=(x + w + INPUT_DX, y),
                    size = (INPUT_X, c_label.GetHeight()))
            c_info.Hide()
            widgets.append(c_info)
            widget_map[path] = c_info
            y += h + INPUT_DY
        return widget_map, widgets, containers
 
    def buttons(self, bitmap, buttons):
        x = ox = bitmap.GetWidth()  - BUTTON_DX
        y =      bitmap.GetHeight() - BUTTON_DY
        row = False
        h = 0
        for button in buttons[::-1]:
            w, h = button.size()
            if row and x - w < BUTTON_SPACING_X:
                row = False
                x = ox
                y -= h + BUTTON_SPACING_Y
            row = True
            x -= w
            button.set_pos(x, y - h)
            x -= BUTTON_SPACING_X
        x = ox
        y -= h + h + BUTTON_SPACING_Y
        return buttons, x, y
        
    def OnEraseBackground(self, event):
        pass
       
    def get_glassy_container(self, bitmap, img, ico, x, y, state):
        return GlassyContainer(self, self.glass, ico, img, bitmap, self.get_set_state(state), x, y)
        
    def init_websites(self):
        websites = self.get_websites()
        widget = self.widget_map['choosewebsite']
        widget.Clear()
        widget.AppendItems(websites)
        
    def set_state(self, state):
        if self.containers:
            for widget in self.containers[3]:
                widget.Hide()
        self.state = state
        back, container, button_list, widgets, init, widget_map = self.container_state[state]
        buttons, self.text_x, self.text_y = self.buttons(back, button_list)
        #self.text_x -= TEXT_LEN
        self.text_x = self.bitmap.GetWidth() - TEXT_LEN
        self.containers = [back, container, buttons, widgets]
        for widget in widgets:
            widget.Show()
        self.widget_map = widget_map
        self.start_op()
        init()
        self.update_containers(self.mouse_pos, 'highlight')
    
    def get_set_state(self, state):
        return lambda: self.set_state(state)
        
    def SetFShape(self, *event):
        region = wx.RegionFromBitmap(self.bitmap)
        self.SetShape(region)
        
    def container_all(self):
        for c in self.containers[1]:
            yield c
        for c in self.containers[2]:
            yield c
       
    def OnLeftDown(self, event):
        self.mouse_pos = event.GetPosition()
        self.pressed_on = self.update_containers(self.mouse_pos, 'press')
        if not self.pressed_on:
            x, y = self.ClientToScreen(self.mouse_pos)
            ox, oy = self.GetPosition()
            if y - oy <= BAR_SIZE:
                dx = x - ox
                dy = y - oy
                self.delta = ((dx, dy))

    def OnLeftUp(self, event):
        self.mouse_pos = event.GetPosition()
        self.update_containers(self.mouse_pos, 'action')
        self.pressed_on = 0
        self.delta = None
    
    def update_containers(self, pos, level):
        count = 0
        if pos:
            new_level = 'highlight' if level == 'action' else level
            for container in self.container_all():
                if level != 'action' and container.press_level == 'press':
                    continue
                if container.region.ContainsPoint(pos):
                    if level == 'action' and container.press_level == 'press':
                        container.action()
                    count += container.set_press_level(new_level)
                else:
                    count += container.set_press_level('off')
            if count: 
                self.Refresh()
        return count
        
    def OnMouseMove(self, event):
        self.mouse_pos = event.GetPosition()
        if not (event.Dragging() and not self.pressed_on):
            self.update_containers(self.mouse_pos, 'highlight')
        elif event.LeftIsDown() and self.delta:
            x, y = self.ClientToScreen(self.mouse_pos)
            self.Move((x - self.delta[0], y - self.delta[1]))
    
    def draw_icon(self, dc, icon):
        dc.DrawBitmap(icon, ICON_DX, ICON_DY, True)
        self.icon_paint = True
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        #dc.SetFont(self.font)
        
        self.icon_paint = False
        
        dc.DrawBitmap(self.containers[0], 0, 0, True)
        
        if self.c_message:
            x = MSG_OX
            y = self.text_y
            for msg in self.c_message:
                dc.DrawText(msg, x, y - TEXT_SIZE)
                y += STAT_SPACING + TEXT_SIZE
            
        for container in self.container_all():
            container.OnPaint(dc)
        if not self.icon_paint and self.state == 'main':
            self.draw_icon(dc, self.inone)
        

if __name__ == "__main__":
    try:
        app = wx.App()
        Gui(None, -1, '')
        app.MainLoop()
    except Exception, e:
        import traceback
        print e
        #print traceback.print_exc(e)
        raw_input()
        