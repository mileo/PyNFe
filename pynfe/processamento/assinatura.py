# -*- coding: utf-8 -*-

import signxml
from OpenSSL import crypto
from pynfe.utils import etree
from pynfe.entidades.certificado import CertificadoA1
from pynfe.utils.flags import NAMESPACE_NFE, NAMESPACE_SIG


class Assinatura(object):
    """Classe abstrata responsavel por definir os metodos e logica das classes
    de assinatura digital."""

    certificado = None
    senha = None

    def __init__(self, certificado, senha):
        self.certificado = certificado
        self.senha = senha

    def assinar(self, xml):
        """Efetua a assinatura da nota"""
        pass

class AssinaturaA1(Assinatura):
    """Classe responsavel por efetuar a assinatura do certificado
    digital no XML informado. Passar XML como string."""

    def assinar(self, xml):
        arquivo_cert = CertificadoA1(self.certificado)
        chave, cert = arquivo_cert.separar_arquivo(self.senha)
        
        #root = etree.parse(xml).getroot()  # caminho
        root = etree.fromstring(xml)  # string
        #root = etree.XML(xml)  # string
        signer = signxml.xmldsig(root, digest_algorithm="sha1")
        signer.sign(method=signxml.methods.enveloped, key=chave, cert=cert,
                    algorithm="rsa-sha1", c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315',
                    reference_uri='#NFe42140903657739000169550020000000011000000011')
        # reference_uri nao funciona
        #verified_data = signer.verify(require_x509=True, ca_pem_file="cert.pem")

        ##chave_id = root.find('.//infNFe[@Id]').attrib['Id']
        #root.findall('.//{http://www.w3.org/2000/09/xmldsig#}Reference')[0] \
        #    .attrib['URI'] = '#chaveteste'

        result = etree.tostring(root, encoding="unicode", pretty_print=True)

        return result
