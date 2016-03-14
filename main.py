#!/usr/bin/env python
import os
import jinja2
import webapp2
from Models import Guestbook
from Praznopolje import praznoime


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("vstopna_stran.html")


class RezultatHandler(BaseHandler):
    def post(self):

        ime = praznoime(self.request.get("ime"))
        priimek = praznoime(self.request.get("priimek"))
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        guestbook = Guestbook(ime=ime, priimek=priimek, email=email, sporocilo=sporocilo)
        guestbook.put()

        params={"guestbook": guestbook}
        return self.render_template("rezultat.html", params=params)


class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query(Guestbook.izbrisan == False).fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_sporocil.html", params=params)

class SeznamSporocilVCakalniciHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query(Guestbook.izbrisan == True).fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_sporocil_v_cakalnici.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)

class PosameznoSporociloVCakalniciHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo_v_cakalnici.html", params=params)


class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
            sporocilo = Guestbook.get_by_id(int(sporocilo_id))
            params = {"sporocilo": sporocilo}
            return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        novo_ime=self.request.get("ime")
        nov_priimek=self.request.get("priimek")
        nov_email=self.request.get("email")
        novo_sporocilo=self.request.get("sporocilo")
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        sporocilo.ime=novo_ime
        sporocilo.priimek=nov_priimek
        sporocilo.email=nov_email
        sporocilo.sporocilo=novo_sporocilo
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = True
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

class PovrniSporociloHandler(BaseHandler):
    def post(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = False
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")

class DokoncnoIzbrisiSporociloHandler(BaseHandler):
    def post(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()
        return self.redirect_to("seznam-sporocil")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler, name="seznam-sporocil"),
    webapp2.Route('/sporocila-v-cakalnici', SeznamSporocilVCakalniciHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo1/<sporocilo_id:\d+>', PosameznoSporociloVCakalniciHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
    webapp2.Route('/sporocilo1/<sporocilo_id:\d+>/povrni', PovrniSporociloHandler),
    webapp2.Route('/sporocilo1/<sporocilo_id:\d+>/dokoncnoizbrisi', DokoncnoIzbrisiSporociloHandler),
], debug=True)