package com.example.demo.model.bean;

import com.example.demo.model.entity.BillDetail;
import jakarta.persistence.Column;
import jakarta.persistence.Id;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
public class BillBean {
    private String billNumber;
    private String billType;
    private String yearMonth;
    private LocalDateTime dateTime;
    private String taxIdNumber;
    private String buyer;
    private String address;
    private Integer total;
    private String taxType;
    private Integer taxNumber;
    private Integer totalAddTax;
    private String chineseTotalAddTax;
    private String includeDateTime;
    private String modifyUserId;
    private String check;
    private String picture;
    private String includeSource;
    private Integer page;
    private List<BillDetail> billDetailList;
}
