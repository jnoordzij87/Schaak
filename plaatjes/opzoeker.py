from globale_enums import StukType , StukKleur

plaatjesOpzoeker = {}

plaatjesOpzoeker[StukType.Koning] = {}
plaatjesOpzoeker[StukType.Dame] = {}
plaatjesOpzoeker[StukType.Toren] = {}
plaatjesOpzoeker[StukType.Loper] = {}
plaatjesOpzoeker[StukType.Paard] = {}
plaatjesOpzoeker[StukType.Pion] = {}

plaatjesOpzoeker[StukType.Koning][StukKleur.Wit] = 'plaatjes/Chess_klt60.png'
plaatjesOpzoeker[StukType.Koning][StukKleur.Zwart] = 'plaatjes/Chess_kdt60.png'
plaatjesOpzoeker[StukType.Dame][StukKleur.Wit] = 'plaatjes/Chess_qlt60.png'
plaatjesOpzoeker[StukType.Dame][StukKleur.Zwart] = 'plaatjes/Chess_qdt60.png'
plaatjesOpzoeker[StukType.Toren][StukKleur.Wit] = 'plaatjes/Chess_rlt60.png'
plaatjesOpzoeker[StukType.Toren][StukKleur.Zwart] = 'plaatjes/Chess_rdt60.png'
plaatjesOpzoeker[StukType.Loper][StukKleur.Wit] = 'plaatjes/Chess_blt60.png'
plaatjesOpzoeker[StukType.Loper][StukKleur.Zwart] = 'plaatjes/Chess_bdt60.png'
plaatjesOpzoeker[StukType.Paard][StukKleur.Wit] = 'plaatjes/Chess_nlt60.png'
plaatjesOpzoeker[StukType.Paard][StukKleur.Zwart] = 'plaatjes/Chess_ndt60.png'
plaatjesOpzoeker[StukType.Pion][StukKleur.Wit] = 'plaatjes/Chess_plt60.png'
plaatjesOpzoeker[StukType.Pion][StukKleur.Zwart] = 'plaatjes/Chess_pdt60.png'