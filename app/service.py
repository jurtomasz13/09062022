from random import randint
import crud


def fight(player, enemy_player):
    LOWER_MULTIPLIER = 0.6
    HIGHER_MULTIPLIER = 1.4

    while player['hp'] > 0 and enemy_player['hp'] > 0:
        player['hp'] -= randint(enemy_player['attack_power']
                                * LOWER_MULTIPLIER, enemy_player['attack_power']*HIGHER_MULTIPLIER)
        if player['hp'] > 0 and enemy_player['hp'] > 0:
            enemy_player['hp'] -= randint(player['attack_power']
                                          * LOWER_MULTIPLIER, player['attack_power']*HIGHER_MULTIPLIER)
    if player['hp'] > 0:
        crud.update_stats(player, enemy_player)
        message = {'winner': player['name']}
    else:
        crud.update_stats(enemy_player, player)
        message = {'winner': enemy_player['name']}
    return message
