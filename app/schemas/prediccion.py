from typing import List
from pydantic import BaseModel
import datetime

class PrediccionDatosEntrada(BaseModel):
    EDAD: float
    INST_CARACTER_ACADEMICO_UNIVERSIDAD: float
    ESTU_METODO_PRGM_PRESENCIAL: float
    ESTU_NSE_IES_4: float
    ESTU_SEMESTRECURSA_9: float
    FAMI_CUANTOSCOMPARTEBAÑO_3_o_4: float  # Corrección: mantener "o"
    FAMI_TIENEMOTOCICLETA_Si: float
    ESTU_COMOCAPACITOEXAMENSB11_Repaso_por_cuenta_propia: float # Corrección: mantener "ó"
    FAMI_TRABAJOLABORMADRE_Trabaja_en_el_hogar_no_trabaja_o_estudia: float # Corrección: mantener espacios
    ESTU_PAGOMATRICULAPROPIO_Si: float
    ESTU_GENERO_M: float
    ESTU_PAGOMATRICULACREDITO_Si: float
    ESTU_VALORMATRICULAUNIVERSIDAD_Mas_de_7_millones: float # Corrección: mantener "Más"
    ESTU_PAGOMATRICULAPADRES_Si: float
    ESTU_HORASSEMANATRABAJA_Mas_de_30_horas: float # Corrección: mantener "Más"
    FAMI_TIENEAUTOMOVIL_Si: float
    FAMI_TIENEHORNOMICROOGAS_Si: float
    ESTU_SEMESTRECURSA_8: float
    FAMI_CUANTOSCOMPARTEBAÑO_2: float
    FAMI_ESTRATOVIVIENDA_Estrato_2: float # Corrección: mantener espacio
    ESTU_PAGOMATRICULABECA_Si: float
    FAMI_TIENESERVICIOTV_Si: float
    FAMI_EDUCACIONMADRE_Secundaria_Bachillerato_completa: float # Corrección: mantener paréntesis
    ESTU_NSE_INDIVIDUAL_2: float
    ESTU_DEPTO_PRESENTACION_BOGOTA: float # Corrección: mantener tilde
    FAMI_ESTRATOVIVIENDA_Estrato_3: float # Corrección: mantener espacio
    
class PrediccionBase(BaseModel):
    questions: List[str]
    url_model: str

class PrediccionOut(BaseModel):
    prediccion: int
    modelo_usado: str

    class Config:
        orm_mode = True