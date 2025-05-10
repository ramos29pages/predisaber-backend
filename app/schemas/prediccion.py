from typing import List
from pydantic import BaseModel, Field, Extra
import datetime

class PrediccionDatosEntrada(BaseModel):
    EDAD: float = 0
    INST_CARACTER_ACADEMICO_UNIVERSIDAD: float = 0
    ESTU_METODO_PRGM_PRESENCIAL: float = 0
    ESTU_NSE_IES_4: float = 0
    ESTU_SEMESTRECURSA_9: float = 0
    FAMI_CUANTOSCOMPARTEBAÑO_3_o_4: float = Field(0, alias="FAMI_CUANTOSCOMPARTEBAÑO_3 o 4")
    FAMI_TIENEMOTOCICLETA_Si: float = 0
    ESTU_COMOCAPACITOEXAMENSB11_Repaso_por_cuenta_propia: float = Field(
        0, alias="ESTU_COMOCAPACITOEXAMENSB11_Repasó por cuenta propia"
    )
    FAMI_TRABAJOLABORMADRE_Trabaja_en_el_hogar_no_trabaja_o_estudia: float = Field(
        0, alias="FAMI_TRABAJOLABORMADRE_Trabaja en el hogar, no trabaja o estudia"
    )
    ESTU_PAGOMATRICULAPROPIO_Si: float = 0
    ESTU_GENERO_M: float = 0
    ESTU_PAGOMATRICULACREDITO_Si: float = 0
    ESTU_VALORMATRICULAUNIVERSIDAD_Mas_de_7_millones: float = Field(
        0, alias="ESTU_VALORMATRICULAUNIVERSIDAD_Más de 7 millones"
    )
    ESTU_PAGOMATRICULAPADRES_Si: float = 0
    ESTU_HORASSEMANATRABAJA_Mas_de_30_horas: float = Field(
        0, alias="ESTU_HORASSEMANATRABAJA_Más de 30 horas"
    )
    FAMI_TIENEAUTOMOVIL_Si: float = 0
    FAMI_TIENEHORNOMICROOGAS_Si: float = 0
    ESTU_SEMESTRECURSA_8: float = 0
    FAMI_CUANTOSCOMPARTEBAÑO_2: float = 0
    FAMI_ESTRATOVIVIENDA_Estrato_2: float = Field(0, alias="FAMI_ESTRATOVIVIENDA_Estrato 2")
    ESTU_PAGOMATRICULABECA_Si: float = 0
    FAMI_TIENESERVICIOTV_Si: float = 0
    FAMI_EDUCACIONMADRE_Secundaria_Bachillerato_completa: float = Field(
        0, alias="FAMI_EDUCACIONMADRE_Secundaria (Bachillerato) completa"
    )
    ESTU_NSE_INDIVIDUAL_2: float = 0
    ESTU_DEPTO_PRESENTACION_BOGOTA: float = Field(0, alias="ESTU_DEPTO_PRESENTACION_BOGOTÁ")
    FAMI_ESTRATOVIVIENDA_Estrato_3: float = Field(0, alias="FAMI_ESTRATOVIVIENDA_Estrato 3")

    
class PrediccionBase(BaseModel):
    questions: List[str]
    url_model: str

class PrediccionOut(BaseModel):
    prediccion: int
    modelo_usado: str

    class Config:
        extra = Extra.ignore  
        allow_population_by_field_name = True
        orm_mode = True