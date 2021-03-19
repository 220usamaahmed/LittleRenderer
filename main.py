from canvas import Canvas


def main():
    canvas = Canvas()    
    canvas.line([0, 100], [100, -50], (255, 255, 255))
    canvas.line([100, -50], [-100, -50], (255, 255, 255))
    canvas.line([-100, -50], [0, 100], (255, 255, 255))
    canvas.show()


if __name__ == "__main__": main()