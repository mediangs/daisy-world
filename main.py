from numpy import sqrt
import pandas as pd
import streamlit as st


def app():
    # AL = alpha
    Tp, SL, sb = 0, None, 0.000000056696  # 지구온도, 태양상수, 슈테판볼츠만 상수
    Ares, Ab, Aw, ALp = None, 0, 0, 0  # Ares, Ab, Aw = 남은면적, 검은데이지 면적, 흰색 데이지 면적,행성반사율

    # ALres, ALb, ALw =  , 검은 데이지의 반사율, 흰 데이지의 반사율
    # F: 열흡수 상수, drD: 데이지의 사망률

    ALres = st.sidebar.slider('ALres', min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    ALb = st.sidebar.slider('검은색데이지 반사율', min_value=0.1, max_value=0.5, value=0.25, step=0.05)
    ALw = st.sidebar.slider('흰색데이지 반사율', min_value=0.5, max_value=1.0, value=0.75, step=0.05)
    ALc = st.sidebar.slider('선인장 반사율', min_value=0.5, max_value=1.0, value=0.9, step=0.05)

    F = 20
    drD = None

    # GFb, GFw =  검은 데이지의 성장률, 흰 데이지의 생장율
    # dAb, dAw = 검은 데이지 면적의 변화율, 흰 데이지 면적의 변화율 , d: 델타
    GFb, GFw, Tb, Tw, dAb, dAw = None, None, None, None, None, None

    # 선인장을 추가하는 내용
    Ac = 0  # Ac: 선인장 면적

    Tc = None # 선인장의 온도
    GFc, dAc  = None, None # 선인장의 성장률, 변화율

    # 양과 늑대를 추가하는 내용
    drsh, drwo = 0.05, 0.05  # 자연적으로 사망하는 양과 늑대.(sh: 양, wo: 늑대)
    dsh, dwo = None, None # 양과 늑대 개체수의 변화율
    Nsh , Nwo = 1500, 500  # 양과 늑대의 초기 개체수
    GNsh, GNwo = None, None # 양과 늑대의 성장률

    time_period = 800
    results=[]

    for time in range(time_period):

        SL = 550 + (5.5 * time) # 태양상수는 조금씩 커짐
        # SL = 400 * sin((double)  time / 35)+550;
        Ares = 1 - Ab - Aw - Ac
        if Ab < 0.0001: Ab=0.0001
        if Aw < 0.0001: Aw=0.0001
        if Ac < 0.0001: Ac=0.0001
        if Nsh <= 0: Nsh=1
        if Nwo <= 0: Nwo=1

        ALp = (Ares * ALres) + (Ab * ALb) + (Aw * ALw) + (Ac * ALc) #데이지 월드의 반사율 --> 온도결정
        Tp = sqrt(sqrt((SL * (1 - ALp)) / sb)) # 데이지 월드의 온도
        Tw = F * (ALp - ALw) + Tp #뭐하는 식이지?
        Tb = F * (ALp - ALb) + Tp
        Tc = F * (ALp - ALc) + Tp
        #Tw, Tb = 흰 데이지가 자라고 있는 지역의 온도, 검은 것.
        GFb = 1 - (0.003265 * (295.5 - Tb) * (295.5 - Tb))
        GFw = 1 - (0.003265 * (295.5 - Tw) * (295.5 - Tw))
        GFc = 1 - (0.003265 * (350 - Tw) * (350 - Tw))

        drD = 0.3 + 0.2 -  1.0 / (Nsh + 2)
        dAb = Ab * (Ares * GFb - drD) # 검은 데이지의 면적의 변화율
        dAw = Aw * (Ares * GFw - drD)
        # dAc = Ac * (Ares * GFc - drD)
        dAc = Ac * (Ares * GFc - 0.3)

        GNsh = (Ab + Aw) * Nsh
        drsh = Nwo * Nsh * 0.0001

        GNwo = Nsh * Nwo * 0.0001
        drwo = Nwo * 0.3

        Nsh = Nsh + GNsh - drsh
        Nwo = Nwo + GNwo - drwo
        Ab = Ab + dAb
        Aw = Aw + dAw
        Ac = Ac + dAc
        if Nsh < 100: Nsh=100
        if Nwo < 100: Nwo=100
        if Ab < 0.0001: Ab=0.0001 # 선을 지키기
        if Aw < 0.0001: Aw=0.0001 # 선을 지키기
        if Ac < 0.0001: Ac=0.0001 # 선을 지키기

        # 출력하는 부분
        results.append({'time': time, 'SL': SL, 'Tp': Tp, 'black-daisy': Ab, 'white-daisy': Aw, 'cactus-area': Ac, 'sheep':Nsh, 'wolf': Nwo})
        # print(f'{time}: 태양상수: {SL:.2f}, 지구온도: {Tp:.2f}, 검은데이지: {Ab:.4f}, 흰색데이지{Aw:.4f}, 선인장면적: {Ac:.4f}, '
        #       f'양: {Nsh:.1f}, 늑대: {Nwo:.1f}')


    df = pd.DataFrame.from_dict(results)
    st.line_chart(df.loc[:, ['white-daisy', 'black-daisy']])
    st.line_chart(df.loc[:, ['sheep', 'wolf']])


if __name__ == '__main__':
    app()
