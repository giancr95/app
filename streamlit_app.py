import calendar
from datetime import date

import streamlit as st


def last_day_of_month(target_date: date) -> date:
    last_day = calendar.monthrange(target_date.year, target_date.month)[1]
    return date(target_date.year, target_date.month, last_day)


def get_month_quincena_range(target_date: date, quincena: int) -> tuple[date, date]:
    if quincena == 1:
        return date(target_date.year, target_date.month, 1), date(target_date.year, target_date.month, 15)
    return date(target_date.year, target_date.month, 16), last_day_of_month(target_date)


st.set_page_config(page_title="Registro de horas y montos", layout="centered")
st.title("Registro de horas y montos")

if "registros" not in st.session_state:
    st.session_state.registros = []
if "filter_start" not in st.session_state:
    st.session_state.filter_start = date.today().replace(day=1)
if "filter_end" not in st.session_state:
    st.session_state.filter_end = last_day_of_month(date.today())

st.subheader("Filtros de fecha")
filter_cols = st.columns([1, 1, 1])
with filter_cols[0]:
    if st.button("Quincena 1 (1–15)", use_container_width=True):
        start, end = get_month_quincena_range(date.today(), 1)
        st.session_state.filter_start = start
        st.session_state.filter_end = end
with filter_cols[1]:
    if st.button("Quincena 2 (16–fin)", use_container_width=True):
        start, end = get_month_quincena_range(date.today(), 2)
        st.session_state.filter_start = start
        st.session_state.filter_end = end
with filter_cols[2]:
    if st.button("Mes completo", use_container_width=True):
        st.session_state.filter_start = date.today().replace(day=1)
        st.session_state.filter_end = last_day_of_month(date.today())

filter_start = st.date_input("Fecha inicio", value=st.session_state.filter_start)
filter_end = st.date_input("Fecha fin", value=st.session_state.filter_end)

if filter_start > filter_end:
    st.error("El rango de fechas es inválido. La fecha inicio debe ser menor o igual a la fecha fin.")
else:
    st.session_state.filter_start = filter_start
    st.session_state.filter_end = filter_end

st.subheader("Nuevo registro")
with st.form("registro_form"):
    registro_fecha = st.date_input("Fecha del registro", value=date.today())
    registro_monto = st.number_input("Monto", min_value=0.0, step=0.01, format="%.2f")
    registro_horas = st.number_input("Horas", min_value=0.0, step=0.5, format="%.2f")
    registro_detalle = st.text_input("Detalle (opcional)")
    submit = st.form_submit_button("Guardar")

if submit:
    errors = []
    if registro_fecha is None:
        errors.append("Debe seleccionar una fecha válida.")
    if registro_monto <= 0:
        errors.append("El monto debe ser positivo.")
    if registro_horas < 0:
        errors.append("Las horas no pueden ser negativas.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.session_state.registros.append(
            {
                "fecha": registro_fecha,
                "monto": registro_monto,
                "horas": registro_horas,
                "detalle": registro_detalle,
            }
        )
        st.success("Registro guardado correctamente.")

st.subheader("Registros filtrados")
registros_filtrados = [
    registro
    for registro in st.session_state.registros
    if st.session_state.filter_start <= registro["fecha"] <= st.session_state.filter_end
]

if registros_filtrados:
    st.dataframe(registros_filtrados, use_container_width=True)
else:
    st.info("No hay registros en el rango seleccionado.")
