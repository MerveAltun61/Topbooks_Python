from BookInfo import BookInfo
from collections import Counter
class Manager:     

    def __init__(self):
        pass

    def read_books_from_file(self, filename):     
        booklist = []                         
        try:                                    
            with open(filename, 'r') as file:   
                for line in file:               
                    if '***' not in line:   
                     line = line.strip()           
                     if line:                       
                       if " by " in line:
                         pos_begin = line.find(".")
                         pos_end = line.find(" by ")
                         pos_downloadnum = line.find(" (")
                         title = line[pos_begin+1:pos_end]
                         author = line[pos_end+4:pos_downloadnum]	
                         downloads = line[pos_downloadnum+2:-1]
                         bookinfo = BookInfo(title, author, downloads)
                         booklist.append(bookinfo)
                       else:
                         pos_begin = line.find(".")
                         pos_downloadnum = line.find(" (")
                         title = line[pos_begin+1:pos_downloadnum]
                         author = "Unknown"
                         downloads = line[pos_downloadnum+2:-1]
                         bookinfo = BookInfo(title, author, downloads)
                         booklist.append(bookinfo)
                        
        except FileNotFoundError:
            print(f"Datei {filename} nicht gefunden.") 
        return booklist                                   


    
    def count_titles(self, booklist):
        title_counter = Counter()                 #title_counter ist ein dictionary

        for book in booklist:
            title = book.get_title().strip()
            title_counter[title] += 1
        return title_counter 

    def display_titles_sorted_alphabetically(self, title_counter):
    
        sorted_titles = sorted(title_counter.items(), key=lambda item: item[0].lower())     # Dann ist title_counter.items() eine Liste von (Schlüssel, Wert)-Tupeln: (Pride&Prejudice:2)
                                                                                            # lambda item: item[0].lower() ist eine anonyme Funktion, die für jedes Element in der Liste (also jedes (title, count)-Tupel) folgendes tut:
                                                                                            # item[0] → greift auf den Titel (also den ersten Teil des Tupels) zu
                                                                                            #.lower() → macht den Titel kleingeschrieben, damit die Sortierung nicht durch Groß-/Kleinschreibung verfälscht wird
        for title, count in sorted_titles:
            print(f'{title}: {count}x')

    
    def get_downloads_per_title(self, booklist):
        downloads_per_title = {}

        for book in booklist:                               
            title = book.get_title().strip()
            downloads = book.get_downloads()

            if title in downloads_per_title:
                downloads_per_title[title] += downloads
            else:
                downloads_per_title[title] = downloads

        return downloads_per_title

    def display_sorted_titles_by_downloads(self, downloads_per_title):
    
        sorted_downloads = sorted(downloads_per_title.items(), key=lambda item: item[1], reverse=True)

        print(f"Top Bücher nach Downloads:")
        for i, (title, downloads) in enumerate(sorted_downloads, start=1):
            print(f"{i}: {downloads}-> {title}")

    def get_downloads_per_author(self, booklist):
        downloads_per_author = {}
        total_downloads = 0

        for book in booklist:
            author = book.get_author().strip()
            try:
                downloads = int(book.get_downloads())
            except ValueError:
                downloads = 0 

            if author in downloads_per_author:
                downloads_per_author[author] += downloads
            else:
                downloads_per_author[author] = downloads
            
            total_downloads += downloads

        if total_downloads == 0: 
            print("Keine gültigen Downloadzahlen gefunden.")
            return {}
    
        author_percentages = {}
        for author, downloads in downloads_per_author.items():
            percentage = (downloads / total_downloads) * 100
            author_percentages[author] = percentage
        return author_percentages

    def sort_author_percentages(self, author_percentages):
         sorted_authors = sorted(author_percentages.items(), key=lambda item: item[1], reverse=True)
         return sorted_authors

    def display_percentages(self, sorted_authors):
        
        print(f"Top Autoren nach Downloads:")
        for i, (author, percent) in enumerate(sorted_authors, start=1):
            print(f"{i}: {percent: .2f}% -> {author}")

        return sorted_authors    

    def write_author_percentages_to_file(self, sorted_authors):
        chosen_filename = input("Bitte geben Sie den Namen der Ausgabedatei an (z.B. autoren_statistik.txt): ").strip()
    
        try:
            with open(chosen_filename, 'w', encoding='utf-8') as file:             
                file.write("Top Autoren nach prozentualem Downloadanteil:\n")
                for i, (author, percent) in enumerate(sorted_authors, start=1):
                    file.write(f"{i}: {percent:.2f}% -> {author}\n")
            print(f"Die Statistik wurde erfolgreich in '{chosen_filename}' gespeichert.")
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei: {e}")


    def main_menu(self):                                
        
        booklist = []      
        sorted_authors = []       

        while True:                                                             
            print("\nMenü:")
            print("[1] Textdatei einlesen und Gesamtzahl ausgeben")
            print("[2] Häufigkeit der einzelnen Titel ausgeben") 
            print("[3] Neue Gesamtreihenfolge ausgeben") #Beliebtheit durch Sortierung Gesamt-Downloadanzahl
            print("[4] Autoren nach Häufigkeit ausgeben")
            print("[5] Autoren nach Häufigkeit in Textdatei ausgeben")
            print("[9] Programm beenden")                                         

            choice = input("Ihre Auswahl: ").strip()                            

            if choice == '1':
                
                filename = "Topbooks/TopBooks.txt"                      
                booklist = self.read_books_from_file(filename)   

                if not booklist:                               
                   print("Keine Bücher verfügbar.")        
                   return   
                  
                print(f"Es wurden {len(booklist)} Bücher eingelesen.") 

            elif choice == "2":
                
                title_counter = self.count_titles(booklist)
                self.display_titles_sorted_alphabetically(title_counter)

            elif choice == '3':
                         
                downloads_per_title = self.get_downloads_per_title(booklist)
                self.display_sorted_titles_by_downloads(downloads_per_title)
            elif choice == '4':
                           
                download_sum = self.get_downloads_per_author(booklist)
                sorted_authors = self.sort_author_percentages(download_sum)
                self.display_percentages(sorted_authors)
                
            elif choice == '5':
                self.write_author_percentages_to_file(sorted_authors)
                
            elif choice == '9':
                print("Programm beendet.")
                break
            else:
                print("Ungültige Auswahl. Bitte erneut versuchen.")             


if __name__ == "__main__": 
   manager_object = Manager()
   manager_object.main_menu()