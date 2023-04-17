#!/bin/bash
dt=$(date +%F'_'%H-%M-%S)
function rpm_check {
        file_output=$(file $package | grep RPM)
        if [ ! -z "$file_output" ]
        then
                echo 0
        else
                echo 1
        fi
}

Help()
{
   # Display Help
   echo -e "\nUsage: \n"
   echo -e "This script will copy the rpms from dropbox to utilities repo"
   echo -e "Drop the RPM in /opt/drop_pack/el8 or /opt/drop_pack/el9 and run the below commands"
   echo
   echo -e "\tSyntax: repo_refresh [-d] [-s el8 or el9] [-f el8 or el9] or repo_refresh el8|el9 (for interactive input for each package)"
   echo -e "\n\toptions:\n"
   echo -e "\t  -s <el8> or <el9>  - Skip the existing packages in the repo"
   echo -e "\t  -f <el8> or <el9>  - Replace the existing packages in the repo"
   echo -e "\t  -d                 - Delete the packages at source"
   echo
   exit 1
}

option_s=false
option_d=false
option_f=""
scount=0
fcount=0


param=$1
while getopts ":ds:f:" option; do
   case $option in
      s ) output='n'
          param=${OPTARG}
          if [ $fcount -gt 0 ]; then
            echo -e "\nOption -s and -f cannot be used together"
            Help
          fi
          if [ $scount -gt 0 ]; then
            echo -e "\nOption -s can only be used Once"
            Help
          fi  
          option_choosed="You have choosed to skip files"
          option_s=true
          scount=1
         ;;
      f ) output='y'
          param=${OPTARG}
          if [ $scount -gt 0 ]; then
            echo -e "\nOption -s and -f cannot be used together"
            Help
          fi
          if [ $fcount -gt 0 ]; then
            echo -e "\nOption -f can only be used Once"
            Help
          fi  
          option_choosed="You have choosed to replace the files"
          option_f=true
          fcount=1
         ;;
      d ) delete_skip='y'
          option_choosed_del="Skipped files will be deleted"
          option_d=true
         ;;
      \? ) 
          Help
          ;;
     
    esac
done

if $option_d && (! $option_s && [[ -z "$option_f" ]]); then
    echo -e "\n Option -d should be used with either -s or -f and el8 or el9"
    exit 1
fi

if [ -n "$param" ]
then
        case $param in
                el8 ) repo_name=lpsx-utils-el8;repo_path=/miscrepos/lpsx-utils-el8;drop_path=/opt/drop_pack/el8;;
                el9 ) repo_name=lpsx-utils-el9;repo_path=/miscrepos/lpsx-utils-el9;drop_path=/opt/drop_pack/el9;;
                * ) echo -e "Please provide the valid option.\nThe Supported Repos are el8 and el9";Help;;
        esac
        log_dir=/opt/drop_pack/logs
        rpm_list=''
        non_rpm_list=''
        skipped_files=''
        if [ ! -d ${log_dir} ]
        then
                mkdir -p $log_dir
        fi
        log_name=${log_dir}/repo_refresh_${param}_${dt}
        echo -e "\n============================================" | tee -a $log_name
        echo -e "\nRefreshing ${repo_name} Repo at $dt" | tee -a $log_name
        echo -e "\n============================================" | tee -a $log_name
        packs=$( ls -ltr $drop_path | grep '^-' | awk '{print $9}' )
        echo $option_choosed >> $log_name
        if [ -n "${packs[@]}" ]
        then
                i=0
                for package in $packs
                do
                        file_validity=$(rpm_check $package)
                        if [ $file_validity -eq 0 ]
                        then
                                file_exist=${repo_path}/${package}
                                if [ -f $file_exist ]
                                then
                                        if [ -n "$output" ]
                                        then
                                                yn=$output
                                        else
                                                read -p "${package} exist in $repo_name, do you want to replace y/n?" yn
                                        fi
                                        while true; do
                                        case $yn in
                                                [yY] ) echo -e "Replacing $package in lpsx-utils-$param" | tee -a $log_name;rm -f $file_exit;cp -f ${drop_path}/${package} ${file_exist};i=$((i+1));rpm_list+=' '${package}' ';break;;
                                                [nN] ) echo -e "Skipping ${package}" | tee -a $log_name;skipped_files+=' '${package}' ';break;;
                                                * ) echo -e "\nPlease Choose the Right Option" | tee -a $log_name ;
                                                        read -p "do you want to replace y/n?" yn;;
                                        esac
                                        done
                                else
                                        echo -e "\nCopying file ${package} to ${file_exist}" | tee -a $log_name
                                        cp -vf ${drop_path}/${package} $file_exist >> $log_name
                                        rpm_list+=' '${package}' '
                                        i=$((i+1))
                                fi
                        else
                                echo -e "\n$package is Not a RPM file" | tee -a $log_name
                                non_rpm_list+=' '${package}' '
                                continue
                        fi
                done
                if [ $i -gt 0 ]
                then
                        createrepo /var/www/${repo_name} | tee -a $log_name
                        if [ $? -eq 0 ]
                        then
                                echo -e "\n${repo_name} repo refreshed succesfully, removing the files from the source dir" | tee -a $log_name
                                for rpm in ${rpm_list[@]}
                                do
                                        rm -f ${drop_path}/$rpm
                                        echo -e "\nRemoved ${drop_path}/$rpm " &>> $log_name
                                done
                                if [ -n "${non_rpm_list[@]}" ]
                                then
                                        for non_rpm in ${non_rpm_list[@]}
                                        do
                                                rm -f ${drop_path}/$non_rpm
                                                echo -e "\nRemoved ${drop_path}/$non_rpm " &>> $log_name
                                        done
                                fi

                        else
                                echo -e "\n${repo_name} repo refreshed unsuccesfully" | tee -a $log_name
                        fi
                fi
        else
                echo -e "\nNo packages were found in the $drop_path" | tee -a $log_name
                exit 1
        fi
        if [ -n "${skipped_files[@]}" ]
        then
                if [ -z "${delete_skip}" ]
                then
                        read -p "Do you want to delete the skipped files? y/n : " ans
                else
                        ans=$delete_skip
                        echo ${option_choosed_del} >> ${log_name}
                fi
                while true; do
                      case $ans in
                           [yY] ) for skip in ${skipped_files[@]}; do echo Removing ${drop_path}/${skip} &>> ${log_name};rm -f ${drop_path}/${skip} &>> ${log_name};done;break;;
                           [nN] ) echo -e "Skipping files from deletion" &>> ${log_name};break;;
                              * ) echo -e "\nPlease Choose the Right Option" | tee -a $log_name ;
                                  read -p "do you want to replace y/n?" ans;;
                      esac
                done

        fi
        echo -e "\nlog can be found in $log_name"
else
        Help
fi
