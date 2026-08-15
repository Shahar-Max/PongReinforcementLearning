import sys
from game_engine import PongEngine
from pong_renderer import PongRenderer

def main():
    WIDTH, HEIGHT = 800, 600
    engine = PongEngine(WIDTH, HEIGHT)
    renderer = PongRenderer(WIDTH, HEIGHT, "Pong - Wall Challenge")

    running = True
    while running:
        quit_requested, up_pressed, down_pressed = renderer.check_events()
        if quit_requested:
            running = False

        # Step the core game logic
        engine.step(up_pressed=up_pressed, down_pressed=down_pressed)

        # Delegate drawing to PongRenderer
        renderer.render(
            engine=engine,
            score_label="Score",
            score_val=engine.score
        )

        # Control FPS using the renderer's tick method
        renderer.tick(60)

        if engine.game_lost:
            running = False

    renderer.close()
    sys.exit()

if __name__ == "__main__":
    main()
