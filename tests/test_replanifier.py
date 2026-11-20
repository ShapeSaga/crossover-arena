"""Changement d'horaires : les posts Buffer déjà programmés sont supprimés puis recréés sur les nouveaux créneaux."""
from datetime import datetime, timedelta, timezone

from robot.etat import PROGRAMME, PUBLIE, VALIDE
from robot.publieurs.base import Resultat
from test_youtube import monde  # noqa: F401  (faux serveurs déjà prêts)


class FauxBuffer:
    def __init__(self):
        self.supprimes, self.crees = [], []

    def supprimer(self, pid):
        self.supprimes.append(pid)

    def programmer(self, pub):
        self.crees.append(pub); return Resultat(id_distant=f"n{len(self.crees)}", message="ok")

    def places_disponibles(self, p):
        return None


def test_videos_programmees_passent_aux_nouveaux_horaires(monde):
    o, s, t = monde
    t[0] = datetime(2026, 11, 20, 23, 45, tzinfo=timezone.utc)
    o.conf["cadence"]["creneaux"] = ["02:00", "21:00"]
    b = FauxBuffer()
    o._publieurs = {p: b for p in ("youtube", "tiktok", "instagram")}
    meta = {"titre": "T", "hashtags": ["#shorts"]}
    o.etat.episodes.clear()
    o.etat.episodes["EP015"] = {"statut": PROGRAMME, "creneau": "2026-11-21T11:00:00+00:00", "meta": meta, "message_id": 1,
                                "video_url": "u15", "programme": {p: {"id": f"a-{p}"} for p in ("youtube", "tiktok", "instagram")}}
    o.etat.episodes["EP016"] = {"statut": PROGRAMME, "creneau": "2026-11-21T19:00:00+00:00", "meta": meta, "message_id": 2,
                                "video_url": "u16", "programme": {p: {"id": f"b-{p}"} for p in ("youtube", "tiktok", "instagram")}}
    o.etat.episodes["EP011"] = {"statut": PUBLIE, "creneau": "2026-11-19T11:00:00+00:00", "meta": meta, "video_url": "u11",
                                "relance_yt": "2026-11-23T11:00:00+00:00", "relances_yt": 1, "programme": {"youtube": {"id": "r11"}}}
    o.replanifier()
    assert sorted(b.supprimes) == sorted([f"{x}-{p}" for x in "ab" for p in ("youtube", "tiktok", "instagram")] + ["r11"])
    assert o.etat.episodes["EP015"]["statut"] == VALIDE
    assert o.etat.episodes["EP015"]["creneau"] == "2026-11-21T20:00:00+00:00"      # 21 h Paris
    assert o.etat.episodes["EP016"]["creneau"] == "2026-11-22T01:00:00+00:00"      # 2 h Paris
    assert "relance_yt" not in o.etat.episodes["EP011"] and o.etat.episodes["EP011"]["relances_yt"] == 0
    o.publier_valides()
    assert len(b.crees) == 6 and {p.date.isoformat() for p in b.crees} == {"2026-11-21T20:00:00+00:00", "2026-11-22T01:00:00+00:00"}
    assert o.etat.episodes["EP015"]["statut"] == PROGRAMME
    o.replanifier()                                                                  # une seule fois
    assert len(b.supprimes) == 7
