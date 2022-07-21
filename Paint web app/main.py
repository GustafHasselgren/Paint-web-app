from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# TODO
#   Nu:
#   Hantera Paints & Methods                                X
#   Feedback - Message flash                                X
#   Fixa Mobile media
#   
#   Snart:
#   Utöka Paints - Typ, Tillverkare, Färg-grupp - Sortera på Färg>Typ
#   Lös 'Hover' på kort
#   
#   Kul längre fram:
#   Stats - Mest använda färg, vanligaste steget, etc.
#