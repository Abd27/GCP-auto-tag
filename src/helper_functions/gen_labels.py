import datetime

def gen_labels(creator_email: str):
    current_date=datetime.date.today().strftime("%Y-%m-%d")
    return {
                'created-by'   : creator_email.replace('@', '_', ).replace('.', '-'),
                'created-date' : current_date
    }
