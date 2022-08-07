import pcbnew
import math

class BGA:
    def __init__(self, board, reference, track, via, logger):
        self.logger = logger
        self.board = board
        self.reference = reference
        self.track = track
        self.via = via
        self.pitchx = 0
        self.pitchy = 0
        self.tracks = []

        self.logger.info(reference)
        self.radian_pad = 0.0
        self.footprint = self.board.FindFootprintByReference(reference)
        self.radian = self.footprint.GetOrientationRadians()
        self.degrees = self.footprint.GetOrientationDegrees()
        self.pads = self.footprint.Pads()
        self.x0 = self.footprint.GetPosition().x
        self.y0 = self.footprint.GetPosition().y
        self.init_data()
    
    def init_data(self):
        if self.degrees not in [0.0 , 90.0, 180.0, -90.0]:
            degrees = self.degrees + 45.0
            self.footprint.SetOrientationDegrees(degrees)
            self.radian_pad = self.footprint.GetOrientationRadians()
            self.footprint.SetOrientationDegrees(0)
        pos_x = []
        pos_y = []

        minx = self.pads[0].GetPosition().x
        maxx = self.pads[0].GetPosition().x
        miny = self.pads[0].GetPosition().y
        maxy = self.pads[0].GetPosition().y

        pos_x.append([self.pads[0].GetPosition()])
        pos_y.append([self.pads[0].GetPosition()])
        
        for pad in self.pads:
            pos = pad.GetPosition()
            if minx > pos.x:
                minx = pos.x
            if maxx < pos.x:
                maxx = pos.x
            if miny > pos.y:
                miny = pos.y
            if maxy < pos.y:
                maxy = pos.y
            checkx = True
            for arr in pos_x:
                if arr[0].y == pos.y and pos not in arr:
                    checkx = False
                    arr.append(pos)
            if checkx == True:
                pos_x.append([pos])
            
            checky = True
            for arr in pos_y:
                if arr[0].x == pos.x and pos not in arr:
                    checky = False
                    arr.append(pos)
            if checky == True:
                pos_y.append([pos])
            
        for arrs in pos_x:
            arrs.sort(key=lambda x:x.x)
        for arrs in pos_y:
            arrs.sort(key=lambda x:x.y)
        
        self.pitchx = pos_x[0][1].x - pos_x[0][0].x
        for arrs in pos_x:
            for i in range(len(arrs)):
                if i > 0:
                    pitch = arrs[i].x - arrs[i-1].x
                    if pitch > 0 and pitch < self.pitchx:
                        self.pitchx = pitch
        
        self.pitchy = pos_y[0][1].y - pos_y[0][0].y
        for arrs in pos_y:
            for i in range(len(arrs)):
                if i > 0:
                    pitch = arrs[i].y - arrs[i-1].y
                    if pitch > 0 and pitch < self.pitchy:
                        self.pitchy = pitch
        self.logger.info('pitch x: %d' %self.pitchx)
        self.logger.info('pitch y: %d' %self.pitchy)
        """
        for ind, arrs in enumerate(pos_y):
            self.logger.info('%d. sort---------------------' %ind)
            for i, arr in enumerate(arrs):
                self.logger.info('%d. %s' %(i, str(arr)))
        """
        self.footprint.SetOrientationDegrees(self.degrees)
        """
        if self.degrees in [0.0 , 90.0, 180.0, -90]:
            x = (minx + maxx)/2
            y = (miny + maxy)/2
            xstart = pcbnew.wxPoint(x, maxy)
            xend = pcbnew.wxPoint(x, miny)
            ystart = pcbnew.wxPoint(minx, y)
            yend = pcbnew.wxPoint(maxx, y)
            xtrack = pcbnew.PCB_TRACK(self.board)
            xtrack.SetStart(xstart)
            xtrack.SetEnd(xend)
            xtrack.SetWidth(self.track)
            xtrack.SetLayer(pcbnew.F_Cu)
            self.board.Add(xtrack)

            ytrack = pcbnew.PCB_TRACK(self.board)
            ytrack.SetStart(ystart)
            ytrack.SetEnd(yend)
            ytrack.SetWidth(self.track)
            ytrack.SetLayer(pcbnew.F_Cu)
            self.board.Add(ytrack)
        else:
            anphalx = (-1)*math.tan(self.radian)
            anphaly = 1/math.tan(self.radian)
            bx = self.y0 - anphalx*self.x0
            by = self.y0 - anphaly*self.x0

            # y = ax + b
            xyminx = anphalx*minx + bx
            xymaxx = anphalx*maxx + bx
            xstart = pcbnew.wxPoint(minx, xyminx)
            xend = pcbnew.wxPoint(maxx, xymaxx)

            yyminx = anphaly*minx + by
            yymaxx = anphaly*maxx + by
            ystart = pcbnew.wxPoint(minx, yyminx)
            yend = pcbnew.wxPoint(maxx, yymaxx)

            xtrack = pcbnew.PCB_TRACK(self.board)
            xtrack.SetStart(xstart)
            xtrack.SetEnd(xend)
            xtrack.SetWidth(self.track)
            xtrack.SetLayer(pcbnew.F_Cu)
            self.board.Add(xtrack)

            ytrack = pcbnew.PCB_TRACK(self.board)
            ytrack.SetStart(ystart)
            ytrack.SetEnd(yend)
            ytrack.SetWidth(self.track)
            ytrack.SetLayer(pcbnew.F_Cu)
            self.board.Add(ytrack)
            #######
            anx = -1*math.tan(self.radian_pad)
            any = 1/math.tan(self.radian_pad)
            b1 = self.y0 - anx*self.x0
            b2 = self.y0 - any*self.x0
            y1 = anx*minx + b1
            y2 = anx*maxx + b1

            y3 = any*minx + b2
            y4 = any*maxx + b2
            start1 = pcbnew.wxPoint(minx, y1)
            end1 = pcbnew.wxPoint(maxx, y2)

            start2 = pcbnew.wxPoint(minx, y3)
            end2 = pcbnew.wxPoint(maxx, y4)

            track1 = pcbnew.PCB_TRACK(self.board)
            track1.SetStart(start1)
            track1.SetEnd(end1)
            track1.SetWidth(self.track)
            track1.SetLayer(pcbnew.F_Cu)
            self.board.Add(track1)

            track2 = pcbnew.PCB_TRACK(self.board)
            track2.SetStart(start2)
            track2.SetEnd(end2)
            track2.SetWidth(self.track)
            track2.SetLayer(pcbnew.F_Cu)
            self.board.Add(track2)
        pcbnew.Refresh()
        """
        
    def fanout(self):
        if self.degrees in [0.0 , 90.0, 180.0, -90.0]:
            for pad in self.pads:
                pos = pad.GetPosition()
                net = pad.GetNetCode()
                if pos.y > self.y0:
                    if pos.x > self.x0:
                        # bottom-right 225
                        x = pos.x + self.pitchx/2
                        y = pos.y + self.pitchy/2
                    else:
                        # bottom-left 135
                        x = pos.x - self.pitchx/2
                        y = pos.y + self.pitchy/2
                    end = pcbnew.wxPoint(x, y)
                    self.add_track(net, pos, end)
                    self.add_via(net, end)
                else:
                    if pos.x > self.x0:
                        # top-right 315
                        x = pos.x + self.pitchx/2
                        y = pos.y - self.pitchy/2
                    else:
                        # top-left 45
                        x = pos.x - self.pitchx/2
                        y = pos.y - self.pitchy/2
                    end = pcbnew.wxPoint(x, y)
                    self.add_track(net, pos, end)
                    self.add_via(net, end)
        elif self.degrees in [45.0 , 135.0, -135.0, -45.0]:
            bx = self.y0 + self.x0
            by = self.y0 - self.x0
            pitch = math.sqrt(self.pitchx*self.pitchx + self.pitchy*self.pitchy)/2
            for pad in self.pads:
                pos = pad.GetPosition()
                net = pad.GetNetCode()
                y1 = bx - pos.x
                y2 = by + pos.x
                if pos.y > y1:
                    if pos.y > y2:
                        # bottom
                        x = pos.x
                        y = pos.y + pitch
                    else:
                        # left
                        x = pos.x + pitch
                        y = pos.y
                    end = pcbnew.wxPoint(x, y)
                    self.add_track(net, pos, end)
                    self.add_via(net, end)
                else:
                    if pos.y > y2:
                        # right
                        x = pos.x - pitch
                        y = pos.y
                    else:
                        # top
                        x = pos.x
                        y = pos.y - pitch
                    end = pcbnew.wxPoint(x, y)
                    self.add_track(net, pos, end)
                    self.add_via(net, end)
        else:
            anphalx = (-1)*math.tan(self.radian)
            anphaly = 1/math.tan(self.radian)
            bx0 = self.y0 - anphalx*self.x0
            by0 = self.y0 - anphaly*self.x0
            
            pax = -1*math.tan(self.radian_pad)
            pay = 1/math.tan(self.radian_pad)
            pitch = math.sqrt(self.pitchx*self.pitchx + self.pitchy*self.pitchy)/2
            for pad in self.pads:
                pos = pad.GetPosition()
                net = pad.GetNetCode()
                y1 = anphalx*pos.x + bx0
                y2 = anphaly*pos.x + by0
                pbx = pos.y - pax*pos.x
                pby = pos.y - pay*pos.x

                # d^2 = (x - x0)^2 + (y - y0)^2
                #     = (x - x0)^2 + (a.x + b - y0)^2
                #     = #x^2 - #2x.x0 + #x0^2 + #a^2.x^2 + #a.b.x - #a.y0.x + #a.b.x + #b^2 - #b.y0 - #a.y0.x - b.y0 + y0^2
                # = (1 + a.a)x.x = (-2.x0 + 2.a.b - 2.a.y0)x + (x0.x0 + b.b - 2.b.y0 + y0.y0) - d.d
                ax = pax*pax + 1
                bx = 2*pax*pbx - 2*pos.x - 2*pax*pos.y
                cx = pos.x*pos.x + pbx*pbx + pos.y*pos.y - 2*pbx*pos.y - pitch*pitch

                ay = pay*pay + 1
                by = 2*pay*pby - 2*pos.x - 2*pay*pos.y
                cy = pos.x*pos.x + pby*pby + pos.y*pos.y - 2*pby*pos.y - pitch*pitch

                deltax = bx*bx - 4*ax*cx
                deltay = by*by - 4*ay*cy
                if deltax > 0:
                    x1 = (-(bx) + math.sqrt(deltax))/(2*ax)
                    x2 = (-(bx) - math.sqrt(deltax))/(2*ax)
                if deltay > 0:
                    x3 = (-(by) + math.sqrt(deltay))/(2*ay)
                    x4 = (-(by) - math.sqrt(deltay))/(2*ay)
                if pos.y > y1:
                    if pos.y > y2:
                        # bottom-left
                        x = x2
                        y = pax*x + pbx
                    else:
                        # bottom-right
                        x = x3
                        y = pay*x + pby
                    end = pcbnew.wxPoint(x, y)
                    self.add_track(net, pos, end)
                    self.add_via(net, end)
                else:
                    if pos.y > y2:
                        # top-left
                        x = x4
                        y = pay*x + pby
                    else:
                        # bottom-right
                        x = x1
                        y = pax*x + pbx
                    end = pcbnew.wxPoint(x, y)
                    self.add_track(net, pos, end)
                    self.add_via(net, end)
        pcbnew.Refresh()
    
    def add_track(self, net, start, end):
        track = pcbnew.PCB_TRACK(self.board)
        track.SetStart(start)
        track.SetEnd(end)
        track.SetWidth(self.track)
        track.SetLayer(pcbnew.F_Cu)
        track.SetNetCode(net)
        self.board.Add(track)
        self.tracks.append(track)
    
    def add_via(self, net, pos):
        via = pcbnew.PCB_VIA(self.board)
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetPosition(pos)
        via.SetWidth(int(self.via.m_Diameter))
        via.SetDrill(self.via.m_Drill)
        via.SetNetCode(net)
        self.board.Add(via)
        self.tracks.append(via)

    def remove_track_via(self):
        for item in self.tracks:
            self.board.Remove(item)
        pcbnew.Refresh()