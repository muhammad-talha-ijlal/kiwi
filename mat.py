import matplotlib.backends.backend_pdf as pdf
import matplotlib.pyplot as plt
import numpy as np

def plot(data, id=1):
    try:
        pdf_pages = pdf.PdfPages(f'visualization{id}.pdf')

        keywords = [d['Keyword'] for d in data]
        total_services = [int(d['Total Services']) for d in data]
        online_services = [int(d['Online Servies']) for d in data]
        total_ratings = [d['Total Ratings on First Page'] for d in data]
        average_ratings = [d['Average Rating'] for d in data]
        average_prices = [d['Average Starting Price'] for d in data]
        median_prices = [d['Median Starting Price'] for d in data]

        related_keywords = []
        for d in data:
            related_keywords.append(list(d['Related Keywords'].keys()))

        # Plot 1: Total Services vs Online Services
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(keywords, total_services, label='Total Services')
        ax.bar(keywords, online_services, label='Online Services')
        ax.set_xlabel('Keywords')
        ax.set_ylabel('Count')
        ax.set_title('Total Services vs Online Services')
        ax.legend()
        pdf_pages.savefig()
        plt.close()

        # Plot 2: Total Ratings
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(keywords, total_ratings)
        ax.set_xlabel('Keywords')
        ax.set_ylabel('Total Ratings')
        ax.set_title('Total Ratings')
        pdf_pages.savefig()
        plt.close()

        # Plot 3: Average Rating, Average Starting Price, Median Starting Price
        fig, ax = plt.subplots(figsize=(10, 6))
        width = 0.25
        x = np.arange(len(keywords))
        rects1 = ax.bar(x - width, average_ratings, width, label='Average Rating')
        rects2 = ax.bar(x, average_prices, width, label='Average Starting Price')
        rects3 = ax.bar(x + width, median_prices, width, label='Median Starting Price')

        # Readings on bars
        for rect in rects1:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        for rect in rects2:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        for rect in rects3:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')

        ax.set_xticks(x)
        ax.set_xticklabels(keywords, rotation=45)
        ax.set_ylabel('Value')
        ax.set_title('Average Rating, Average Starting Price, and Median Starting Price')
        ax.legend()
        pdf_pages.savefig()
        plt.close()

        # Plot 4: Related Keyword
        for i, related_keyword in enumerate(related_keywords):
            fig, ax = plt.subplots(figsize=(10, 6))
            related_keyword_labels = list(data[i]['Related Keywords'].keys())
            related_keyword_counts = list(data[i]['Related Keywords'].values())
            ax.bar(related_keyword_labels, related_keyword_counts)
            ax.set_xlabel('Related Keywords')
            ax.set_ylabel('Count')
            ax.set_title(f'Related Keywords for {keywords[i]}')
            plt.xticks(rotation=45)
            pdf_pages.savefig()
            plt.close()

        pdf_pages.close()
    except:
        pass