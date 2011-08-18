import wsdlprovider
import binascii
import rhinoscriptsyntax as rs
import os


class Shapeways3d:
    wsdl_url = "http://api.shapeways.com/v1/wsdl.php"
    application_id = "rhino3d"
    username = rs.GetString("enter shapeways username")
    password = rs.GetString("enter shapeways password")
    assembly = wsdlprovider.GetWebservice(wsdl_url)
    shapelink = assembly.SWwsdlService()
    session_id = shapelink.login(username, password, application_id)
    def getprinters(self):
        if self.session_id:
            #get list of printers available
            printers = self.shapelink.getPrinters(self.session_id, "", self.application_id)
            if printers: return printers
    def getprice(self,volume,material):
        if self.session_id:
            #get price
            price = self.shapelink.getModelPrice(self.session_id,volume,material, "", self.application_id)
            if price: return price
    def submit(self):
        if self.session_id:
            model = self.assembly.SWModel()
            stlreader = open(os.path.abspath("c:/users/public/swm.stl"))
            model.file = tuple(bytearray((stlreader.read()),"base64"))
            stlreader.close()
            model.title = "test"
            model.desc = "test"
            model.modeltype = "STL"
            model.filename = "test"
            model.tags = "test"
            model.has_color = 0
            model.scale = .01
            model.markup = 1.0
            loaded = self.shapelink.submitModel(self.session_id,model,"", self.application_id)
            os.remove(os.path.abspath("c:/users/public/swm.stl"))
            return loaded


if __name__=="__main__":   
    obj = rs.GetObject("object to print",False,False,24,False)
    rs.ObjectName(obj,"swm.stl")
    rs.UnselectAllObjects()
    rs.Command ("_-Export _selname swm.stl _enter c:\users\public\swm.stl _enter _enter")
    rs.ObjectName(obj,"")
    printsession = Shapeways3d()
    isloaded = printsession.submit()
    print isloaded