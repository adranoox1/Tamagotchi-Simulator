# Tamagotchi-Simulator
User stories

Written as “As a player, I want… so that…”, grouped by feature. They describe what, not how, so they stay valid whatever you decide above.

Epic 1 – The pets

US1. As a player, I want three pets to exist when the game starts, so that I have something to take care of.
US2. As a player, I want to see a pet’s name and its four stats, so that I know what it needs.

Epic 2 – Care actions

US3. As a player, I want to feed my pet, so that its hunger goes down.
US4. As a player, I want to play with my pet, so that its boredom goes down (knowing it gets hungrier and more tired).
US5. As a player, I want to put my pet to sleep, so that its exhaustion goes down.
US6. As a player, I want to heal my pet, so that its health goes up.
US7. As a player, I want stats to stay within limits, so that values never become absurd (negative, or above the max).

Epic 3 – Time, life and death

US8. As a player, I want pets’ stats to evolve after each action, so that neglect has consequences.
US9. As a player, I want a pet to die when its health reaches zero, so that the game has stakes.
US10. As a player, I want random events to sometimes happen, so that the game is less predictable.

Epic 4 – Menu

US11. As a player, I want a menu that reappears after each action, so that I can keep playing.
US12. As a player, I want to select which pet I’m taking care of, so that my actions apply to the right one.
US13. As a player, I want to quit the game from the menu.

Epic 5 – Statistics

US14. As a player, I want to see how many pets are alive and dead.
US15. As a player, I want to see the average health of living pets and the average hunger, boredom and exhaustion.

Epic 6 – Save and load

US16. As a player, I want to save the game (all pets, their stats, alive/dead), so that I can stop and come back later.
US17. As a player, I want to load a saved game, so that I continue exactly where I left off.

Epic 7 – Robustness

US18. As a player, if I type something invalid in the menu, I want an error message instead of a crash.
US19. As a player, if I select a pet that doesn’t exist, I want to be told and asked again.
US20. As a player, if I try to act on a dead pet, I want to be told it’s dead.
US21. As a player, if the save file is missing or broken, I want a clear message and the game to keep running.

Suggested order
Sprint 1: US1, US2, US3–US7 (the class, tested without a menu)
Sprint 2: US11, US12, US13 (playable game)
Sprint 3: US8, US9, US10 (the game becomes a game)
Sprint 4: US14, US15, US16, US17
Sprint 5: US18–US21, then final testing