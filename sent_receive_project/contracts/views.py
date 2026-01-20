from datetime import timedelta, timezone, datetime
from django.utils.text import slugify
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from sent_items.utils import calc_cart_total
from toners.utils import calc_toner_stock_alert
from .models import Contracts
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile, File


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def view_contract_details(request):
    contracts = Contracts.objects.all().order_by('-purchased_date')
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"contracts": contracts,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen}
    # # Check if any contract has no PDF file associated
    # no_pdf_contracts = [contract for contract in contracts if not contract.pdf_file]
    #
    # # If there are contracts without PDF files, pass a flag to the template
    # if no_pdf_contracts:
    #     context['no_pdf_contracts'] = True
    return render(request, 'view_contract_details.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def add_contract_details(request):
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total,"toner_stock_alert":toner_stock_alert,"toner_under_fifteen":toner_under_fifteen,
               "purchased_by_choice": Contracts.purchased_by_choice,"warranty_range":Contracts.warranty_range}
    return render(request, 'add_contract_details.html',context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
# def contract_details_save(request):
#     if request.method == "POST":
#         lpo_no = request.POST.get('lpo_no', '').strip()
#
#         if lpo_no == "":
#             messages.error(request, "LPO Number is empty")
#             return redirect('add_contract_details')
#
#         if Contracts.objects.filter(lpo_no=lpo_no).exists():
#             messages.error(request, "LPO Number already exists")
#             return redirect('add_contract_details')
#         else:
#             contracts = Contracts()
#             contracts.lpo_no = lpo_no
#             contracts.purchased_by = request.POST.get("purchased_by")
#             # contracts.date_purchased = request.POST.get("date_purchased")
#             contracts.warranty_years = int(request.POST.get("warranty_years", 0))
#
#             # Convert date_purchased to a datetime object
#             # date_purchased = datetime.strptime(contracts.date_purchased,
#             #                                    "%Y-%m-%d").date() if contracts.date_purchased else None
#             # Parse date_purchased string to datetime
#             try:
#                 contracts.purchased_date = datetime.strptime(request.POST.get("purchased_date"), "%Y-%m-%d").date()
#             except ValueError:
#                 messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
#                 return redirect('add_contract_details')
#
#             contracts.warranty_start = contracts.purchased_date
#
#             # Check if the request has a file associated with the key 'pdf_file'
#             if 'pdf_file' in request.FILES:
#                 new_pdf_file = request.FILES['pdf_file']
#                 new_filename = f"{slugify(lpo_no)}_{new_pdf_file.name}"
#                 contracts.pdf_file.save(new_filename, ContentFile(new_pdf_file.read()))
#
#             if contracts.warranty_start:
#                 # Calculate warranty_end based on warranty_years
#                 contracts.warranty_end = contracts.warranty_start + timedelta(days=contracts.warranty_years * 365)
#                 contracts.save()
#                 messages.success(request, "Contract Added Successfully")
#                 return redirect('view_contract_details')
#             else:
#                 messages.error(request, "Invalid date purchased")
#                 return redirect('add_contract_details')
#     else:
#         return redirect('view_contract_details')
def contract_details_save(request):
    if request.method == "POST":
        lpo_no = request.POST.get('lpo_no', '').strip()

        if lpo_no == "":
            messages.error(request, "LPO Number is empty")
            return redirect('add_contract_details')

        if Contracts.objects.filter(lpo_no=lpo_no).exists():
            messages.error(request, "LPO Number already exists")
            return redirect('add_contract_details')
        else:
            contracts = Contracts()
            contracts.lpo_no = lpo_no
            contracts.purchased_by = request.POST.get("purchased_by")

            # Parse purchased_date string to datetime
            try:
                contracts.purchased_date = datetime.strptime(request.POST.get("purchased_date"), "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return redirect('add_contract_details')

            # Check if warranty is not applicable
            warranty_na = request.POST.get("warranty_na")
            if warranty_na:
                contracts.warranty_years = 0
            else:
                contracts.warranty_years = int(request.POST.get("warranty_years", 0))

            contracts.warranty_start = contracts.purchased_date
            contracts.warranty_end = contracts.warranty_start + timedelta(days=contracts.warranty_years * 365)

            # Check if the request has a file associated with the key 'pdf_file'
            if 'pdf_file' in request.FILES:
                new_pdf_file = request.FILES['pdf_file']
                new_filename = f"{slugify(lpo_no)}_{new_pdf_file.name}"
                contracts.pdf_file.save(new_filename, ContentFile(new_pdf_file.read()))

            contracts.save()

            messages.success(request, "Contract Added Successfully")
            return redirect('view_contract_details')
    else:
        return redirect('view_contract_details')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def contract_delete(request, id):
    contracts = Contracts.objects.get(id=id)
    contracts.delete()
    messages.success(request, "Contract Deleted Successfully")
    return redirect('view_contract_details')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_contract_details(request, id):
    contracts = Contracts.objects.get(id=id)
    data_calc_cart_total = calc_cart_total(request)
    cart_total = data_calc_cart_total['cart_total']
    data_calc_toner_stock_alert = calc_toner_stock_alert(request)
    toner_stock_alert = data_calc_toner_stock_alert['toner_stock_alert_count']
    toner_under_fifteen = data_calc_toner_stock_alert['tonerstock']
    context = {"total": cart_total, "contracts": contracts,"toner_stock_alert":toner_stock_alert,
               "toner_under_fifteen":toner_under_fifteen,"purchased_by_choice": Contracts.purchased_by_choice,
               "warranty_range":Contracts.warranty_range}
    return render(request, 'edit_contract_details.html', context)


# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @login_required(login_url="login")
# def edit_contract_details_save(request):
#     if request.method == "POST":
#         contract_id = request.POST.get("contract_id")
#         lpo_no = request.POST.get("lpo_no").strip()
#         if lpo_no == "":
#             messages.error(request, "LPO Number is empty")
#             return redirect('view_contract_details')
#
#         else:
#             warranty_years = int(request.POST.get("warranty_years", 0))
#             purchased_by = request.POST.get("purchased_by")
#             try:
#                 purchased_date = datetime.strptime(request.POST.get("purchased_date"), "%Y-%m-%d").date()
#             except ValueError:
#                 messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
#                 return redirect('view_contract_details')
#
#             warranty_start = purchased_date
#             if warranty_start:
#                 # Calculate warranty_end based on warranty_years
#                 warranty_end = warranty_start + timedelta(days=warranty_years * 365)
#                 Contracts_model = Contracts(id=contract_id, lpo_no=lpo_no, warranty_years=warranty_years,
#                                             purchased_by=purchased_by, purchased_date=purchased_date,
#                                             warranty_end=warranty_end,warranty_start = purchased_date)
#                 Contracts_model.save()
#
#                 messages.success(request, "Contract Edited Successfully")
#                 return redirect('view_contract_details')
#             else:
#                 messages.error(request, "Invalid date purchased")
#                 return redirect('add_contract_details')
#     else:
#         return redirect('view_contract_details')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def edit_contract_details_save(request):
    if request.method == "POST":
        contract_id = request.POST.get("contract_id")
        lpo_no = request.POST.get("lpo_no").strip()
        if lpo_no == "":
            messages.error(request, "LPO Number is empty")
            return redirect('view_contract_details')

        else:
            warranty_years = int(request.POST.get("warranty_years", 0))
            purchased_by = request.POST.get("purchased_by")
            try:
                purchased_date = datetime.strptime(request.POST.get("purchased_date"), "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return redirect('view_contract_details')

            warranty_start = purchased_date
            if warranty_start:
                # Calculate warranty_end based on warranty_years
                warranty_end = warranty_start + timedelta(days=warranty_years * 365)
                new_pdf_file = request.FILES.get('pdf_file')
                existing_contract = Contracts.objects.get(id=contract_id)

                # Check if the LPO number is changed
                if existing_contract.lpo_no != lpo_no:
                    # Rename the file on the file system
                    if existing_contract.pdf_file:
                        old_path = existing_contract.pdf_file.path
                        new_filename = f"{slugify(lpo_no)}_{existing_contract.pdf_file.name.split('_')[-1]}"
                        new_path = os.path.join(os.path.dirname(old_path), new_filename)
                        os.rename(old_path, new_path)

                        # Update the database value for pdf_file
                        existing_contract.pdf_file.name = f"pdfs/contracts/{new_filename}"

                # Remove the existing file only if a new file is uploaded
                if new_pdf_file:
                    if existing_contract.pdf_file:
                        default_storage.delete(existing_contract.pdf_file.name)
                    # Save the new file with the new filename based on the LPO number
                    new_filename = f"{slugify(lpo_no)}_{new_pdf_file.name}"
                    existing_contract.pdf_file.save(new_filename, ContentFile(new_pdf_file.read()))



                existing_contract.lpo_no = lpo_no
                existing_contract.warranty_years = warranty_years
                existing_contract.purchased_by = purchased_by
                existing_contract.purchased_date = purchased_date
                existing_contract.warranty_start = warranty_start
                existing_contract.warranty_end = warranty_end
                existing_contract.save()

                messages.success(request, "Contract Edited Successfully")
                return redirect('view_contract_details')
            else:
                messages.error(request, "Invalid date purchased")
                return redirect('add_contract_details')
    else:
        return redirect('view_contract_details')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url="login")
def contracts(request):
    return HttpResponse("this is for the contracts page")