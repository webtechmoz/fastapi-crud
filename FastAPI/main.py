import flet as ft
import asyncio
import httpx

async def main(page: ft.Page):
    page.title = 'API'
    page.window.width = 450
    page.window.height = 650

    # Definindo as variáveis
    width: int = 450
    height: int = 650

    textfields = {
        'hint_text': ['Nome', 'Username', 'Email', 'Senha'],
        'Icon': [ft.icons.PERSON, ft.icons.PERSON, ft.icons.EMAIL, ft.icons.KEY],
        'password': [False, False, False, True]
    }

    #Criar Usuário
    async def criar(e: ft.ControlEvent):
        dados = {}

        for text_value in text_values.controls:
            text_value: ft.TextField
            if text_value.value != '':
                dados.setdefault(text_value.hint_text.lower(), text_value.value)
                text_value.value = ''

        if len(dados) == 4:
            url = f'http://127.0.0.1:8000/usuarios/inserir'
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=dados)
            
            if response.status_code == 200:
                await listar_usuarios()
        
            page.update()

    #Editar Usuário
    async def editar_email(e: ft.ControlEvent, id: int):
        dados = {}

        for text_value in text_values.controls:
            text_value: ft.TextField
            if text_value.hint_text == 'Email':
                if text_value.value != '':
                    dados.setdefault('email', text_value.value)

                    url = f'http://127.0.0.1:8000/usuarios/editar_email/{id}'
                    async with httpx.AsyncClient() as client:
                        response = await client.put(url, json=dados)
                    
                    if response.status_code == 200:
                        await listar_usuarios()
                    
                    text_value.value = ''
                
                page.update()
                break

    #Apagar Usuário
    async def apagar(e: ft.ControlEvent, id: int):
        url = f'http://127.0.0.1:8000/usuarios/apagar/{id}'
        async with httpx.AsyncClient() as client:
            response = await client.delete(url)
        
        if response.status_code == 200:
            await listar_usuarios()
        
        else:
            print(response.json())

    # Listar Usuarios
    async def listar_usuarios():
        url = 'http://127.0.0.1:8000/usuarios'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            if len(response.json()) > 0:
                tabela.rows.clear()

                try:
                    for usuario in response.json()['usuarios']:
                        tabela.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        content=ft.Row(
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.icons.EDIT,
                                                    icon_color=ft.colors.BLUE,
                                                    on_click=lambda e, id= usuario[0]: asyncio.run(editar_email(e, id))
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.DELETE,
                                                    icon_color=ft.colors.RED,
                                                    on_click=lambda e, id= usuario[0]: asyncio.run(apagar(e, id))
                                                )
                                            ]
                                        )
                                    ),
                                    ft.DataCell(
                                        content=ft.Text(
                                            value=usuario[0]
                                        )
                                    ),
                                    ft.DataCell(
                                        content=ft.Text(
                                            value=usuario[1]
                                        )
                                    ),

                                    ft.DataCell(
                                        content=ft.Text(
                                            value=usuario[2]
                                        )
                                    )
                                ]
                            )
                        )
                
                except:
                    pass
            
            page.update()

    # Definindo a interface do sistema
    main = ft.Container(
        bgcolor=ft.colors.with_opacity(0.02, 'black'),
        width=width - 50,
        height=height,
        padding=ft.padding.only(
            top=10,
            left=8,
            right=8
        ),
        border_radius=10,

        content=ft.Column(
            controls=[
                ft.Text(
                    value='Usuários',
                    size=20,
                    weight='bold',
                    color=ft.colors.with_opacity(0.4, 'black')
                ),
                ft.Divider(
                    height=1,
                    thickness=2,
                    color=ft.colors.with_opacity(0.2, 'black')
                ),

                text_values := ft.Column(
                    controls=[
                        ft.TextField(
                            hint_text=textfields['hint_text'][i],
                            hint_style=ft.TextStyle(
                                size=14,
                                color=ft.colors.with_opacity(0.4, 'black'),
                                weight='bold'
                            ),
                            text_style=ft.TextStyle(
                                size=14,
                                color=ft.colors.with_opacity(0.8, 'black'),
                                weight='bold'
                            ),
                            prefix_icon=textfields['Icon'][i],
                            password=textfields['password'][i],
                            autofocus=True

                        ) for i in range(len(textfields['hint_text']))
                    ]
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.FloatingActionButton(
                            text='Criar Usuario',
                            foreground_color='white',
                            bgcolor='blue',
                            col={'xs': 12},
                            height=40,
                            on_click= lambda e: asyncio.run(criar(e))
                        )
                    ]
                ),

                ft.Column(
                    controls=[
                        tabela := ft.DataTable(
                            show_bottom_border=True,
                            columns=[
                                ft.DataColumn(ft.Text(value='gerir')),
                                ft.DataColumn(ft.Text(value='id')),
                                ft.DataColumn(ft.Text(value='nome')),
                                ft.DataColumn(ft.Text(value='username')),
                            ],

                            rows=[

                            ]
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    height=height * 0.35
                )
            ]
        )
    )

    await listar_usuarios()
    page.add(main)

if __name__ == '__main__':
    ft.app(target=main)