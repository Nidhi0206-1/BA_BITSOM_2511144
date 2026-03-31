import requests
from datetime import datetime

print("Task 1 - File Write and Read")

note1 = "Topic 1: Variables store data. Python is dynamically typed."
note2 = "Topic 2: Lists are ordered and mutable."
note3 = "Topic 3: Dictionaries store key-value pairs."
note4 = "Topic 4: Loops automate repetitive tasks."
note5 = "Topic 5: Exception handling prevents crashes."

f_out = open("python_notes.txt", "w", encoding="utf-8")
f_out.write(note1 + "\n")
f_out.write(note2 + "\n")
f_out.write(note3 + "\n")
f_out.write(note4 + "\n")
f_out.write(note5 + "\n")
f_out.close()
print("File written successfully.")

f_app = open("python_notes.txt", "a", encoding="utf-8")
f_app.write("Topic 6: Functions make code reusable.\n")
f_app.write("Topic 7: Requests fetch data from APIs.\n")
f_app.close()
print("Lines appended.")

print("\nReading file back:")
f_in = open("python_notes.txt", "r", encoding="utf-8")
cnt = 0
for line in f_in:
    cnt = cnt + 1
    # strip the newline
    clean_l = line.strip("\n")
    print(str(cnt) + ". " + clean_l)
f_in.close()

print("\nTotal lines:", cnt)

key_str = input("Enter a keyword to search in notes: ")
f_in2 = open("python_notes.txt", "r", encoding="utf-8")
found_key = False
for line in f_in2:
    if key_str.lower() in line.lower():
        print(line.strip("\n"))
        found_key = True
f_in2.close()

if found_key == False:
    print("Keyword not found in notes.")


print("\n\nTask 3 Part A - Safe Divide")

def safe_divide(a, b):
    try:
        ans = a / b
        return ans
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("safe_divide(10, 2):", safe_divide(10, 2))
print("safe_divide(10, 0):", safe_divide(10, 0))
print("safe_divide('ten', 2):", safe_divide("ten", 2))


print("\n\nTask 3 Part B - File Reader Guard")

def read_file_safe(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        dt = f.read()
        f.close()
        return dt
    except FileNotFoundError:
        print("Error: File '" + filename + "' not found.")
        return ""
    finally:
        print("File operation attempt complete.")

print("\nReading python_notes.txt:")
read_file_safe("python_notes.txt")
print("\nReading ghost_file.txt:")
read_file_safe("ghost_file.txt")


print("\n\nTask 2 - API Integration (& Task 3 Part C)")

print("Fetching products...")
products_list = []

try:
    req_prod = requests.get("https://dummyjson.com/products?limit=20", timeout=5)
    
    if req_prod.status_code == 200:
        json_resp = req_prod.json()
        products_list = json_resp["products"]
        
        print("ID | Title | Category | Price | Rating")
        print("-------------------------------------------------")
        for p in products_list:
            p_id = str(p['id'])
            p_tit = p['title'][:20]
            p_cat = p['category']
            p_pr = str(p['price'])
            p_rt = str(p['rating'])
            print(p_id + " | " + p_tit + " | " + p_cat + " | $" + p_pr + " | " + p_rt)
            
except requests.exceptions.ConnectionError as err:
    print("Connection failed. Please check your internet.")
    now_clk = str(datetime.now())[:19]
    f_lg = open("error_log.txt", "a", encoding="utf-8")
    f_lg.write("[" + now_clk + "] ERROR in fetch_products: ConnectionError - No connection could be made\n")
    f_lg.close()
except requests.exceptions.Timeout as err:
    print("Request timed out. Try again later.")
    now_clk = str(datetime.now())[:19]
    f_lg = open("error_log.txt", "a", encoding="utf-8")
    f_lg.write("[" + now_clk + "] ERROR in fetch_products: Timeout - " + str(err) + "\n")
    f_lg.close()
except Exception as e:
    print("Unknown error:", e)


print("\nFiltering and Sorting Ratings >= 4.5:")
good_rating_items = []
for p in products_list:
    if p["rating"] >= 4.5:
        good_rating_items.append(p)

# student sort usage instead of lambda mapping
def get_pr(x):
    return x["price"]
    
good_rating_items.sort(key=get_pr, reverse=True)

for g in good_rating_items:
    t = g["title"]
    pr = str(g["price"])
    rt = str(g["rating"])
    print(t + " - $" + pr + " (Rating: " + rt + ")")

print("\nLaptop Category Search:")
try:
    req_lap = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
    if req_lap.status_code == 200:
        lap_resp = req_lap.json()
        for lap in lap_resp["products"]:
            n = lap["title"]
            pr = str(lap["price"])
            print("- " + n + " : $" + pr)
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as err:
    print("Unknown error:", err)

print("\nPOST Request Sim:")
my_prod = {
  "title": "My Custom Product",
  "price": 999,
  "category": "electronics",
  "description": "A product I created via API"
}
try:
    req_post = requests.post("https://dummyjson.com/products/add", json=my_prod, timeout=5)
    print("POST Response Data:")
    print(req_post.json())
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as err:
    print("Error:", err)


print("\n\nTask 3 Part D - Input Validation Loop")

while True:
    usr_val = input("Enter a product ID to look up (1-100), or 'quit' to exit: ")
    usr_clean = usr_val.strip()
    if usr_clean.lower() == "quit":
        break
        
    try:
        num = int(usr_clean)
        if num < 1 or num > 100:
            print("Warning: Must be an integer 1-100")
            continue
            
        # Call API
        try:
            url_id = "https://dummyjson.com/products/" + str(num)
            req_id = requests.get(url_id, timeout=5)
            
            if req_id.status_code == 404:
                print("Product not found.")
            elif req_id.status_code == 200:
                id_data = req_id.json()
                print("Found: " + id_data["title"] + " - $" + str(id_data["price"]))
                
        except requests.exceptions.ConnectionError:
            print("Connection failed. Please check your internet.")
        except requests.exceptions.Timeout:
            print("Request timed out. Try again later.")
        except Exception:
            print("Something went wrong with the API call.")

    except ValueError:
        print("Warning: Please enter an integer number.")


print("\n\nTask 4 - Error Logging Test File")

print("Testing Bad Connection")
try:
    bad_conn = requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as err:
    print("Caught bad connection error as expected.")
    rn = str(datetime.now())[:19]
    f_err1 = open("error_log.txt", "a", encoding="utf-8")
    f_err1.write("[" + rn + "] ERROR in fetch_products: ConnectionError - No connection could be made\n")
    f_err1.close()
except Exception:
    pass

print("Testing HTTP 404")
try:
    # 999 doesn't exist
    req_999 = requests.get("https://dummyjson.com/products/999", timeout=5)
    if req_999.status_code != 200:
        print("Caught 404 Not Found error as expected.")
        # log it
        rn = str(datetime.now())[:19]
        f_err2 = open("error_log.txt", "a", encoding="utf-8")
        f_err2.write("[" + rn + "] ERROR in lookup_product: HTTPError - 404 Not Found for product ID 999\n")
        f_err2.close()
except requests.exceptions.ConnectionError:
    pass
except Exception:
    pass

print("\n--- Reading error_log.txt ---")
try:
    final_f = open("error_log.txt", "r", encoding="utf-8")
    log_content = final_f.read()
    print(log_content)
    final_f.close()
except FileNotFoundError:
    print("Error log is empty.")
