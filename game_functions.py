import sys
from bullet import Bullet
from alien import Alien
from time import sleep
import pygame
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    """Fire a bullet if limit is not rewached yet"""
    if len(bullets) < ai_settings.bullets_allowed:
        #Create a new bullet and add it to the bullets group.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keywords and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y) #Only active when game is not active
    if button_clicked and not stats.game_active:
        #Reset the game Settings
        ai_settings.initialize_dynamic_settings()
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        #Reset the game statistics
        stats.reset_stats() #Resetting here means giving player three new ships
        stats.game_active = True
        #Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        #Create a new fleet and center the ship_hit
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()



def update_screen(ai_settings, screen, stats,sb,ship,aliens,bullets, play_button):
    """ Update the game screen and flip to the new screen """
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():  #The bullets.sprites() method returns a list of all sprites in the group bullets.
        bullet.draw_bullet() #To draw all fired bullets to the screen, we loop through the sprites in bullets and call draw_bullet() on each one
    ship.blitme()  #Drawing ship onscreen
    aliens.draw(screen) #Draws each alien in the group to the screen
    #Draw the score information
    sb.show_score()  #To show score just before play button is drawn
    # Draw the play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()
    #Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb,ship, aliens, bullets):
    """ Update positions of the bulet and remove the old bullets """
    #update bullet position
    bullets.update() #automatically calls update() for each sprite in the group
    #Get rid of bullets that have disappeared
    for bullet in bullets.copy(): #We shouldn’t remove items from a list or group within a for loop, so we have to loop over a copy of the group
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb,ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb,ship, aliens, bullets):
        #Check for any bullets that have hit aliens
        #If so get rid of the bullets and aliens
    collisions = pygame.sprite.groupcollide(bullets,aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) ==0:
        #If the entire fleet is destroyed, start a new level.
        #Destroy current bullets and speeding up game and creating a new fleet
        bullets.empty()
        ai_settings.increase_speed()
        #Increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """ Determine the number of aliens in a straight row """
    available_space_x = ai_settings.screen_width - 2 * alien_width #Check horizontal space available for aliens
    number_aliens_x = int(available_space_x / (2 * alien_width)) #Number of aliens that can fit into the space
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """ Determine the number of rows of aliens that fit on the screen """
    available_space_y = ai_settings.screen_height - 3*alien_height - ship_height
    number_rows = int(available_space_y/ (2*alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens,alien_number,row_number):
    """ Create an alien and place it in a row """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """ Create a full fleet of aliens """
    #Create an alien and find the number of the aliens in the row
    #Spacing between each alien is equal to alien's width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height, alien.rect.height)
    #Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Create an alien and place it in row
            create_alien(ai_settings, screen, aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    """ Respond appropriately if any aliens have reached the edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """ Drop the entire fleet and change the fleet's direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #Respond to ship being hit by alien
    if stats.ships_left > 0:
        stats.ships_left -=1
        #Update scoreboard
        sb.prep_ships()
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        #Create a new fleet and center the ship
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(ai_settings,screen,stats,sb, ship,aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
         if alien.rect.bottom >= screen_rect.bottom:
             ship_hit(ai_settings,screen,stats,sb,ship, aliens, bullets)
             break


def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """    Check if the fleet is at an edge,and then update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #Look for alien ship collisions
    #The method spritecollideany() takes two arguments: a sprite and a group.
    #The method looks for any member of the group that’s collided
    #with the sprite and stops looping through the group as soon as it finds one member
    #that has collided with the sprite
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    check_alien_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_high_score(stats,sb):
    """ Check to see if there's a new high score """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
