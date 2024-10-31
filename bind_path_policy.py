#!/usr/bin/env python
##############################################################################
# Import Libraries
##############################################################################
import prisma_sase
import argparse
import sys
import csv
from csv import DictReader
##############################################################################
# Prisma SD-WAN Auth Token
##############################################################################
try:
    from prismasase_settings import PRISMASASE_CLIENT_ID, PRISMASASE_CLIENT_SECRET, PRISMASASE_TSG_ID

except ImportError:
    PRISMASASE_CLIENT_ID=None
    PRISMASASE_CLIENT_SECRET=None
    PRISMASASE_TSG_ID=None



def bind(sase_session, lists_from_csv, policy_name):
   
    #resp = sase_session.get.networkpolicysetstacks()
    policy_id = None
    for policy in sase_session.get.networkpolicysetstacks().cgx_content["items"]:
        if policy["name"] == policy_name:
            policy_id = policy["id"]
    
    if not policy_id:
        print("ERR: No matching policy found")
    
    
    for site in lists_from_csv:
        for site_found in sase_session.get.sites().cgx_content["items"]:
            if site == site_found["name"]:
                if site_found["network_policysetstack_id"] == policy_id:
                    print("Path policy stack is already set to " + policy_name)
                else:
                    site_found["network_policysetstack_id"] = policy_id
                    resp = sase_session.put.sites(site_id = site_found["id"], data=site_found)
                    if not resp:
                        print("Unabled to update path policy stack")
                        return
                    else:
                        print("Updated path policy statck to " + policy_name)          
    
    return


def go():
    #############################################################################
    # Begin Script
    #############################################################################
    parser = argparse.ArgumentParser(description="{0}.".format("Prisma SD-WAN Port Speed Config Details"))
    config_group = parser.add_argument_group('Config', 'Details for the ION devices you wish to update')
    config_group.add_argument("--sites", "-S", help="Source Element Name", default=None)
    config_group.add_argument("--policy_name", "-N", help="Destination Element Name",default=None)

    #############################################################################
    # Parse Arguments
    #############################################################################
    args = vars(parser.parse_args())

    sites = args.get("sites", None)
    if sites is None:
        print("ERR: Invalid Site List. Please provide a CSV file for your site list")
        sys.exit()

    policy_name = args.get("policy_name", None)
    if policy_name is None:
        print("ERR: Invalid Path Policy Name. Please provide a valid Path Policy Name")
        sys.exit()

    ##############################################################################
    # Login
    ##############################################################################
    sase_session = prisma_sase.API()
    sase_session.interactive.login_secret(client_id=PRISMASASE_CLIENT_ID,
                                          client_secret=PRISMASASE_CLIENT_SECRET,
                                          tsg_id=PRISMASASE_TSG_ID)
    if sase_session.tenant_id is None:
        print("ERR: Login Failure. Please provide a valid Service Account")
        sys.exit()
        
    with open(sites, "r") as csvfile:
        csvreader = DictReader(csvfile)
        lists_from_csv = []
        for row in csvreader:
            lists_from_csv.append(row['Site_Name'])
    
    
    bind(sase_session, lists_from_csv, policy_name)
   

    return

if __name__ == "__main__":
    go()