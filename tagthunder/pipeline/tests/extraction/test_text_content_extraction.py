from unittest import TestCase

from pipeline.models.responses import HTMLPP
from pipeline.blocks.extraction.utils.text_content_extraction import TextExtractor

htmlpp = HTMLPP("""
    <h1 is-usable="true">Example title</h1>
    <img is-usable="true" alt="Alternative 1" title="Title 1" src=""/>
    <a is-usable="true" href="https://example.com">Un lien</a>
    <img is-usable="true" alt="Alternative 2" title="Title 2" src=""/>
    <div is-usable="true" title="Title 3">
        <img is-usable="false" alt="Alternative 4" title="Title 4"/>
    </div>
    <div is-usable="true">
        <img is-usable="true" alt="Alternative 5" title="Title 5"/>
        <p is-usable="false">P3</p>
        <p is-usable="false">P4</p>
    </div>
    <p is-usable="true" title="Title P1">P1 <strong is-usable="true">P11</strong> <a is-usable="true" href="https://example.com">P12</a>
    </p>
    <p is-usable="false">P2</p>
""")

htmlpp = HTMLPP("""
<html><body><header bbox="0 0 1185 139.125" id="banner" is-usable="true" role="banner" style="display: block; visibility: visible;" xpath='//*[@id="banner"]'>
<button bbox="447.6875 -46.5625 289.625 46.5625" class="lien_standard texte-couleur3 hover-couleur2 sr-only-focusable" is-usable="true" onclick="tarteaucitron.userInterface.openPanel();" style="display: block; visibility: visible;" type="button" xpath="/html/body/div/header/button">
     Aller à la bannière de cookies
    </button>
<div bbox="0 0 1185 41.28125" class="cal_nav-secondaire hidden-xs" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/div[3]">
<div bbox="0 0 1185 41.28125" class="container-fluid" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]">
<div bbox="15 0 133 41.28125" class="cal_reseaux-sociaux" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[1]">
<div bbox="15 10 133 21.28125" class="reseaux-sociaux" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]">
<a bbox="27 10 17 21.28125" href="/accueil/accessibilite-numerique.html" is-usable="true" style="display: inline-block; visibility: visible;" target="_self" title="Accessibilité Numérique" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[1]">
<img alt="Logo accessibilité" bbox="27 10 17 17" height="17/&gt;" is-usable="true" src="/files/live/sites/calvados/files/documents/images/Accessibilite/a11y.png" style="display: inline-block; visibility: visible;" width="17/&gt;" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[1]/img"/>
</a>
<a bbox="56 13 8 18.28125" href="https://www.facebook.com/CalvadosDep/" is-usable="true" style="display: inline-block; visibility: visible;" target="_blank" title="La page Facebook du Département du Calvados" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[2]">
<img alt="Logo Facebook" bbox="56 13 8 14" height="14/&gt;" is-usable="true" src="/files/live/sites/calvados/files/documents/images/logo-facebook-gris.png" style="display: inline-block; visibility: visible;" width="8/&gt;" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[2]/img"/>
</a>
<a bbox="76 13 16 18.28125" href="https://twitter.com/calvadosdep" is-usable="true" style="display: inline-block; visibility: visible;" target="_blank" title="Le compte Twitter du Département du Calvados" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[3]">
<img alt="Logo Twitter" bbox="76 13 16 14" height="14/&gt;" is-usable="true" src="/files/live/sites/calvados/files/documents/images/logo-twitter-gris.png" style="display: inline-block; visibility: visible;" width="16/&gt;" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[3]/img"/>
</a>
<a bbox="104 13 15 18.28125" href="https://www.instagram.com/calvadosdepartement/" is-usable="true" style="display: inline-block; visibility: visible;" target="_blank" title="Le compte Instagram du Département" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[4]">
<img alt="Le compte Instagram du Département" bbox="104 13 15 14" height="14/&gt;" is-usable="true" src="/files/live/sites/calvados/files/documents/images/logo-instagram-gris.png" style="display: inline-block; visibility: visible;" width="15/&gt;" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[4]/img"/>
</a>
<a bbox="131 10 17 21.28125" href="https://fr.linkedin.com/company/d%C3%A9partementducalvados" is-usable="true" style="display: inline-block; visibility: visible;" target="_blank" title="Le compte LinkedIn du Département" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[5]">
<img alt="Logo LinkedIn" bbox="131 10 17 17" height="17/&gt;" is-usable="true" src="/files/live/sites/calvados/files/documents/images/logo-linkedin-gris-17.png" style="display: inline-block; visibility: visible;" width="17/&gt;" xpath="/html/body/div/header/div[3]/div[1]/div[1]/div[1]/a[5]/img"/>
</a>
</div>
</div>
<div bbox="300.515625 0 869.484375 40" class="cal_liens" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]">
<div bbox="300.515625 8 54.828125 24.84375" class="cal_police" is-usable="true" style="display: inline-block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[1]">
<button aria-disabled="false" bbox="300.515625 14 22.75 16.28125" class="cal_reduire-police" is-usable="true" style="display: inline-block; visibility: visible;" title="A- Diminuer la taille de la police " type="button" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[1]/button[1]">
         A-
        </button>
<button aria-disabled="false" bbox="325.828125 8 29.515625 24.84375" class="cal_augmenter-police" is-usable="true" style="display: inline-block; visibility: visible;" title="A+ Augmenter la taille de la police " type="button" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[1]/button[2]">
         A+
        </button>
</div>
<a bbox="358.125 0 176.734375 40" class="liensIcone entete" href="/contact" is-usable="true" style="display: inline-block; visibility: visible;" target="_blank" title="Vous avez une question, trouvez la réponse" xpath="/html/body/div/header/div[3]/div[1]/div[2]/a[1]">
<span bbox="390.671875 12 129.1875 16" class="libelle" is-usable="true" style="display: inline; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/a[1]/span[2]">
         Contactez-nous
        </span>
</a>
<div bbox="557.640625 0 103.015625 40" class="cal_mag fond-couleur1" is-usable="true" style="display: inline-block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[2]">
<a bbox="572.640625 12 73.015625 16" href="http://emag.calvados.fr" is-usable="true" style="display: inline; visibility: visible;" target="_blank" title="Le magazine numérique du Département du calvados" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[2]/a">
<span bbox="590.109375 12 55.546875 16" class="libelle" is-usable="true" style="display: inline; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[2]/a/span[2]">
          L'E-mag
         </span>
</a>
</div>
<div bbox="663.4375 0 215.375 40" class="linkListMenu dropdown" is-usable="true" style="display: inline-block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/div[3]">
<button aria-expanded="false" aria-haspopup="true" aria-labelledby="tousNosSitesLabel" bbox="678.4375 10 185.375 20" class="dropdown-toggle" data-toggle="dropdown" id="tousNosSites" is-usable="true" style="display: inline-block; visibility: visible;" title="Déployer le menu, tous nos sites web" type="button" xpath='//*[@id="tousNosSites"]'>
<span bbox="695.984375 12 148.09375 16" class="cal_libelle" id="tousNosSitesLabel" is-usable="true" style="display: inline; visibility: visible;" xpath='//*[@id="tousNosSitesLabel"]'>
          Tous nos sites Web
         </span>
</button>
</div>
<a bbox="881.59375 0 187.046875 40" class="liensIcone entete" href="/pres-de-chez-vous" is-usable="true" style="display: inline-block; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/a[2]">
<span bbox="914.140625 12 139.5 16" class="libelle" is-usable="true" style="display: inline; visibility: visible;" xpath="/html/body/div/header/div[3]/div[1]/div[2]/a[2]/span[2]">
         Près de chez vous
        </span>
</a>
</div>
</div>
</div>
<nav arial-label="Menu de navigation" bbox="0 41.28125 1185 97.84375" class="cal_nav-principale cal_desktop hidden-xs affix-top" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/nav">
<div bbox="0 41.28125 324 90.28125" class="cal_logo" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/nav/div[1]">
<a bbox="30 98.28125 264 11" href="/accueil.html" is-usable="true" style="display: inline; visibility: visible;" title="Aller sur la page d'accueil" xpath="/html/body/div/header/nav/div[1]/a">
<img alt="Logo Calvados - Le département" bbox="30 61.28125 264 46" is-usable="true" src="/files/live/sites/calvados/files/documents/images/logo-calvados-transparent.png" style="display: inline-block; visibility: visible;" xpath="/html/body/div/header/nav/div[1]/a/img"/>
</a>
</div>
<ul bbox="402.3125 41.28125 782.6875 97.84375" class="cal_liens" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/nav/ul">
<li bbox="403.3125 41.28125 230.703125 97.84375" class="cal_lien couleur2" is-usable="true" style="display: list-item; visibility: visible;" xpath="/html/body/div/header/nav/ul/li[2]">
<a bbox="404.3125 41.28125 229.703125 92.84375" data-id="9f11993a-8790-49dc-b90b-6b29c7e7cbc3" href="/accueil/le-departement.html" is-usable="true" style="display: block; visibility: visible;" title="Aller sur la page : Le Département" xpath="/html/body/div/header/nav/ul/li[2]/a">
        Le Département
       </a>
</li>
<li bbox="634.015625 41.28125 230.890625 97.84375" class="cal_lien couleur3" is-usable="true" style="display: list-item; visibility: visible;" xpath="/html/body/div/header/nav/ul/li[3]">
<a bbox="635.015625 41.28125 229.890625 92.84375" data-id="c943989d-0aee-4f46-abe2-f5636d5ed895" href="/accueil/aides--services.html" is-usable="true" style="display: block; visibility: visible;" title="Aller sur la page : Aides &amp; services" xpath="/html/body/div/header/nav/ul/li[3]/a">
        Aides &amp; services
       </a>
</li>
<li bbox="864.90625 41.28125 197.09375 97.84375" class="cal_lien couleur1" is-usable="true" style="display: list-item; visibility: visible;" xpath="/html/body/div/header/nav/ul/li[4]">
<a bbox="865.90625 41.28125 196.09375 92.84375" data-id="265b26fb-2fcd-4e39-8824-c39fd6823d27" href="/accueil/toute-linfo.html" is-usable="true" style="display: block; visibility: visible;" title="Aller sur la page : Toute l'info" xpath="/html/body/div/header/nav/ul/li[4]/a">
        Toute l'info
       </a>
</li>
<li bbox="1062 41.28125 123 96.84375" class="cal_recherche recherche_native" is-usable="true" style="display: list-item; visibility: visible;" xpath="/html/body/div/header/nav/ul/li[5]">
<span bbox="1063 86.28125 122 19" is-usable="true" role="search" style="display: inline; visibility: visible;" xpath="/html/body/div/header/nav/ul/li[5]/span">
<button aria-expanded="false" aria-owns="search-popin" bbox="1063 41.28125 122 96.84375" data-id="search" is-usable="true" style="display: inline-block; visibility: visible;" title="Ouvrir la recherche" type="button" xpath="/html/body/div/header/nav/ul/li[5]/span/button">
<span bbox="1107 107.125 1 1" class="sr-only" is-usable="true" style="display: block; visibility: visible;" xpath="/html/body/div/header/nav/ul/li[5]/span/button/span[2]">
          Ouvrir la recherche"
         </span>
</button>
</span>
</li>
</ul>
</nav>
</header></body></html>
""")


class TestTextExtractor(TestCase):
    def test_extract(self):
        txt = TextExtractor.extract(htmlpp)
        print(txt)
        # assert txt == ['Title 1', 'Title 2', 'Title 3', 'Title 5', 'Title P1', 'Alternative 1', 'Alternative 2',
        #                'Alternative 5', 'Example title', 'Un lien', 'P1 P11 P12']
