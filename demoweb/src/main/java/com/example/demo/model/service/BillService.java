package com.example.demo.model.service;

import com.example.demo.model.bean.BillBean;
import org.springframework.web.multipart.MultipartFile;

public interface BillService {
   BillBean findMistakeBill(int page);
   BillBean findMistakeBill();
   BillBean findCorrectBill();
   BillBean findCorrectBill(int page);
   String updateFile(MultipartFile file);
}
