from conexao import conexao, cursor
    
def get_points(email: str, id_jogo: int) -> None|int:
    """
    Return points of user in the game
    
    Parameters
    ----------
    email : str
        email associated with the user
        
    id_game : int
        game id, which the user scored
    
    
    Returns
    -------
        get_points(email, id_game, point) -> int|str
    
    """ 
    cursor.execute("SELECT pt.pontos FROM pontuacao as pt inner join jogadores as jg ON jg.id_jogador = pt.id_jogador WHERE jg.email = %s and pt.id_jogo = %s", (email, id_jogo))
    
    registro = cursor.fetchone()
    
    if registro:
        return registro[0]
    return registro
    

def store_points(email: str, id_jogo: int, pontos: int) -> None:
    """
    Updates the user's score in a specific game storing the new points in the DB
    
    Parameters
    ----------
    email : str
        email associated with the user
        
    id_jogo : int
        game id, which the user scored
        
    pontos : int 
        user score in session
    
    """ 
    points = get_points(email, id_jogo)
    
    if points:
        try:
            cursor.execute("UPDATE pontuacao as pt inner join jogadores as jg on jg.id_jogador = pt.id_jogador SET pt.pontos = pt.pontos + %s WHERE jg.email = %s and pt.id_jogo = %s", (pontos, email, id_jogo))
            conexao.commit()
            return
        except Exception as e:
            print(f"Erro ao atualizar pontos:\n{e}")
        
    try:
        cursor.execute("INSERT INTO pontuacao(id_jogador, id_jogo, pontos) SELECT (select jg.id_jogador from jogadores as jg where jg.email  = %s), %s, %s", (email, id_jogo, pontos))
        conexao.commit()
        return
    except Exception as e:
        print(f"Erro ao inserir pontos:\n{e}")
        
        
def get_game_ranking(id_jogo: int) -> list[dict]:
    """
    Return ranking of a game
    
    Parameters
    ----------
    
    id_game : int
        game id, to search for the ranking
    
    
    Returns
    -------
        get_game_ranking(email, id_game, point) -> list[dict]

    """ 
    
    cursor.execute("SELECT pt.pontos, jg.nome from pontuacao as pt INNER JOIN jogadores as jg ON jg.id_jogador = pt.id_jogador where pt.id_jogo = %s ORDER BY pt.pontos DESC limit 10", (id_jogo,))
     
     
    ranking = sorted([{"nome": jogador[1],"pontos": jogador[0]} for jogador in cursor.fetchall()], key=lambda data_jogador: data_jogador["pontos"], reverse=True)
    return ranking
