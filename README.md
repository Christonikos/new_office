# :office: :question: Where shall we set up the new office?

:exclamation: :moneybag: Finding the optimal coordinates for the installation of a new office is a paramount element of a successful company. 

Here, we present a recommendation algorithm that provides tentative coordinates under an optimization criterion. 

The user needs to provide a set of antagonistic elements (e.g: competitive companies) and a number of synergetic elements (e.g:  collaborators). 

:mag_right: The algorithm will then utilize unsupervised clustering technique to suggest a location that maximizes the distance of the new office from the competitors, while minimizing the distance from the collaborators.     


# :bar_chart: Data
Data mined with the GOOGLE PLACES api. 

# ⚙️ Tools & Techniques
✔️. Data mining/Web Scraping
✔️. Text/Data preprocessing
✔️. Machine Learning (Unsupervised clustering: k-means clustering)
✔️. Python3

# :file_folder: Repository directories
1. Code: The code is standalone and written entirely in a jupyter notebook. 
2. Data: Example data for three Greek cities and the specific case of a new accounting company (Th-Squared).
3. Report: Detailed analysis for the case study of the Th-Squared company.
4. Presentation: A Beamer presentation of the case-study.
